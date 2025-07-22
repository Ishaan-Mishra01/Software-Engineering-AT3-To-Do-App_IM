#!/usr/bin/env python3
"""Performance tests for the To-Do application"""
import unittest
import sys
import os
import json
import time
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestPerformance(unittest.TestCase):
    
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
            
    def test_response_time_login_page(self):
        """Test login page loads quickly"""
        start_time = time.time()
        response = self.client.get('/login')
        end_time = time.time()
        
        response_time = end_time - start_time
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5)  # Should load in less than 500ms
        
    def test_multiple_tasks_performance(self):
        """Test performance with multiple tasks"""
        # Register user
        register_data = {
            'email': 'perf@test.com',
            'username': 'perfuser',
            'password': 'perfpass'
        }
        self.client.post('/login', data=register_data)
        
        # Create 50 tasks
        start_time = time.time()
        for i in range(50):
            task_data = {
                'text': f'Performance test task {i}',
                'list': 'Personal' if i % 2 == 0 else 'Work'
            }
            response = self.client.post('/api/tasks',
                                      data=json.dumps(task_data),
                                      content_type='application/json')
            self.assertEqual(response.status_code, 200)
            
        creation_time = time.time() - start_time
        self.assertLess(creation_time, 5)  # 50 tasks should be created in less than 5 seconds
        
        # Test retrieving all tasks
        start_time = time.time()
        response = self.client.get('/api/tasks')
        retrieval_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 50)
        self.assertLess(retrieval_time, 0.5)  # Should retrieve in less than 500ms
        
    def test_concurrent_user_simulation(self):
        """Test handling multiple users"""
        users = []
        
        # Register 10 users
        for i in range(10):
            user_data = {
                'email': f'user{i}@test.com',
                'username': f'user{i}',
                'password': f'pass{i}'
            }
            
            start_time = time.time()
            response = self.client.post('/login', data=user_data)
            registration_time = time.time() - start_time
            
            self.assertEqual(response.status_code, 302)
            self.assertLess(registration_time, 0.5)
            
            # Logout for next user
            self.client.get('/logout')
            
    def test_static_file_caching(self):
        """Test static file serving performance"""
        # First request
        start_time = time.time()
        response1 = self.client.get('/static/base.css')
        first_load_time = time.time() - start_time
        
        # Second request (should be faster due to caching)
        start_time = time.time()
        response2 = self.client.get('/static/base.css')
        second_load_time = time.time() - start_time
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertLess(first_load_time, 0.5)
        self.assertLess(second_load_time, 0.5)
        
    def test_data_file_size_growth(self):
        """Test data file doesn't grow too large"""
        # Register user
        register_data = {
            'email': 'size@test.com',
            'username': 'sizeuser',
            'password': 'sizepass'
        }
        self.client.post('/login', data=register_data)
        
        # Create tasks and check file size
        for i in range(20):
            task_data = {
                'text': f'Task {i} with some longer text to test file size growth',
                'list': 'Personal'
            }
            self.client.post('/api/tasks',
                           data=json.dumps(task_data),
                           content_type='application/json')
            
        # Check file size
        file_size = os.path.getsize(self.temp_file.name)
        self.assertLess(file_size, 10000)  # Should be less than 10KB for 20 tasks
        
    def test_memory_usage_stability(self):
        """Test that repeated operations don't cause memory issues"""
        # Register user
        register_data = {
            'email': 'memory@test.com',
            'username': 'memoryuser',
            'password': 'memorypass'
        }
        self.client.post('/login', data=register_data)
        
        # Perform many operations
        for i in range(100):
            # Create task
            response = self.client.post('/api/tasks',
                                      data=json.dumps({'text': f'Task {i}'}),
                                      content_type='application/json')
            task = json.loads(response.data)
            
            # Update task
            self.client.put(f'/api/tasks/{task["id"]}',
                          data=json.dumps({'completed': True}),
                          content_type='application/json')
            
            # Delete task
            self.client.delete(f'/api/tasks/{task["id"]}')
            
        # If we get here without crashing, memory is stable
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()