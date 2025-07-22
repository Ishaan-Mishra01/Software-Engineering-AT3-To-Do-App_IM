#!/usr/bin/env python3
"""Integration tests for API endpoints"""
import unittest
import sys
import os
import json
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestAPIIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create temporary data file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.app.config['DATA_FILE'] = self.temp_file.name
        
        # Initialize empty data
        with open(self.app.config['DATA_FILE'], 'w') as f:
            json.dump({'users': {}, 'tasks': {}}, f)
            
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
        try:
            os.unlink(self.temp_file.name)
        except:
            pass
            
    def test_full_user_flow(self):
        """Test complete user registration, login, task management flow"""
        
        # 1. Register new user
        register_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        
        response = self.client.post('/login', data=register_data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        # Check session was created
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user'), 'newuser')
            self.assertEqual(sess.get('email'), 'newuser@example.com')
            
        # 2. Access home page (should work now)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # 3. Create a task
        task_data = {
            'text': 'Integration test task',
            'list': 'Work'
        }
        
        response = self.client.post('/api/tasks',
                                  data=json.dumps(task_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        task = json.loads(response.data)
        self.assertEqual(task['text'], 'Integration test task')
        self.assertEqual(task['list'], 'Work')
        self.assertFalse(task['completed'])
        task_id = task['id']
        
        # 4. Get all tasks
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['text'], 'Integration test task')
        
        # 5. Update task
        update_data = {'completed': True}
        response = self.client.put(f'/api/tasks/{task_id}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        updated_task = json.loads(response.data)
        self.assertTrue(updated_task['completed'])
        
        # 6. Delete task
        response = self.client.delete(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify task was deleted
        response = self.client.get('/api/tasks')
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 0)
        
        # 7. Logout
        response = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        # Verify session was cleared
        with self.client.session_transaction() as sess:
            self.assertNotIn('user', sess)
            self.assertNotIn('email', sess)
            
    def test_login_with_wrong_password(self):
        """Test login with incorrect password"""
        
        # First register a user
        register_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'correctpass'
        }
        self.client.post('/login', data=register_data)
        self.client.get('/logout')  # Logout after registration
        
        # Try to login with wrong password
        login_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpass'
        }
        
        response = self.client.post('/login', data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)
        
    def test_api_authentication(self):
        """Test that API endpoints require authentication"""
        
        # Try to access tasks without login
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 401)
        
        error = json.loads(response.data)
        self.assertEqual(error['error'], 'Not logged in')
        
        # Try to create task without login
        response = self.client.post('/api/tasks',
                                  data=json.dumps({'text': 'Test'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 401)
        
    def test_task_not_found(self):
        """Test updating/deleting non-existent task"""
        
        # Register and login
        register_data = {
            'email': 'test@example.com',
            'username': 'test',
            'password': 'test123'
        }
        self.client.post('/login', data=register_data)
        
        # Try to update non-existent task
        response = self.client.put('/api/tasks/nonexistent',
                                 data=json.dumps({'completed': True}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)
        
        error = json.loads(response.data)
        self.assertEqual(error['error'], 'Task not found')
        
    def test_multiple_users_isolation(self):
        """Test that users can only see their own tasks"""
        
        # Register first user
        user1_data = {
            'email': 'user1@example.com',
            'username': 'user1',
            'password': 'pass1'
        }
        self.client.post('/login', data=user1_data)
        
        # Create task for user1
        response = self.client.post('/api/tasks',
                                  data=json.dumps({'text': 'User 1 task'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Logout user1
        self.client.get('/logout')
        
        # Register second user
        user2_data = {
            'email': 'user2@example.com',
            'username': 'user2',
            'password': 'pass2'
        }
        self.client.post('/login', data=user2_data)
        
        # User2 should see no tasks
        response = self.client.get('/api/tasks')
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 0)
        
        # Create task for user2
        response = self.client.post('/api/tasks',
                                  data=json.dumps({'text': 'User 2 task'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify user2 only sees their task
        response = self.client.get('/api/tasks')
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['text'], 'User 2 task')

if __name__ == '__main__':
    unittest.main()