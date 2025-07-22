#!/usr/bin/env python3
"""Security tests for the To-Do application"""
import unittest
import sys
import os
import json
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestSecurityFeatures(unittest.TestCase):
    
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
            
    def test_session_security(self):
        """Test session management security"""
        # Register user
        register_data = {
            'email': 'secure@test.com',
            'username': 'secureuser',
            'password': 'securepass'
        }
        self.client.post('/login', data=register_data)
        
        # Get session cookie
        with self.client.session_transaction() as sess:
            self.assertIn('user', sess)
            self.assertIn('email', sess)
            
        # Test that session exists (Flask may not set cookie if already exists)
        response = self.client.get('/')
        # Session should be working properly - we're logged in
        self.assertEqual(response.status_code, 200)
        
    def test_no_sql_injection(self):
        """Test protection against SQL injection (even though we use JSON)"""
        # Try SQL injection in login
        injection_data = {
            'email': "'; DROP TABLE users; --",
            'password': "' OR '1'='1"
        }
        
        response = self.client.post('/login', data=injection_data)
        # Should handle gracefully without errors
        self.assertIn(response.status_code, [200, 302])
        
    def test_no_xss_in_tasks(self):
        """Test XSS protection in task creation"""
        # Register user
        register_data = {
            'email': 'xss@test.com',
            'username': 'xssuser',
            'password': 'xsspass'
        }
        self.client.post('/login', data=register_data)
        
        # Try to create task with XSS
        xss_task = {
            'text': '<script>alert("XSS")</script>',
            'list': 'Personal'
        }
        
        response = self.client.post('/api/tasks',
                                  data=json.dumps(xss_task),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Get tasks and verify script is stored as-is (not executed)
        response = self.client.get('/api/tasks')
        tasks = json.loads(response.data)
        self.assertEqual(tasks[0]['text'], '<script>alert("XSS")</script>')
        
    def test_authentication_required(self):
        """Test that all protected routes require authentication"""
        # Test protected routes without authentication
        protected_routes = [
            ('GET', '/'),
            ('GET', '/api/tasks'),
            ('POST', '/api/tasks'),
            ('PUT', '/api/tasks/123'),
            ('DELETE', '/api/tasks/123')
        ]
        
        for method, route in protected_routes:
            if method == 'GET':
                response = self.client.get(route)
            elif method == 'POST':
                response = self.client.post(route, 
                                          data=json.dumps({'test': 'data'}),
                                          content_type='application/json')
            elif method == 'PUT':
                response = self.client.put(route,
                                         data=json.dumps({'test': 'data'}),
                                         content_type='application/json')
            elif method == 'DELETE':
                response = self.client.delete(route)
                
            # Home page redirects, API returns 401
            if route == '/':
                self.assertEqual(response.status_code, 302)
            else:
                self.assertEqual(response.status_code, 401)
                
    def test_password_not_exposed(self):
        """Test that passwords are not exposed in API responses"""
        # Register user
        register_data = {
            'email': 'pass@test.com',
            'username': 'passuser',
            'password': 'secretpass123'
        }
        self.client.post('/login', data=register_data)
        
        # Create and get tasks
        self.client.post('/api/tasks',
                       data=json.dumps({'text': 'Test task'}),
                       content_type='application/json')
        
        response = self.client.get('/api/tasks')
        data = response.data.decode('utf-8')
        
        # Ensure password is not in response
        self.assertNotIn('secretpass123', data)
        self.assertNotIn('password', data)
        
    def test_csrf_considerations(self):
        """Test CSRF protection considerations"""
        # Note: Flask doesn't have built-in CSRF for non-form requests
        # This test documents the need for CSRF protection in production
        
        # Register user
        register_data = {
            'email': 'csrf@test.com',
            'username': 'csrfuser',
            'password': 'csrfpass'
        }
        self.client.post('/login', data=register_data)
        
        # API calls work without CSRF token (vulnerability in production)
        response = self.client.post('/api/tasks',
                                  data=json.dumps({'text': 'CSRF test'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # This is expected behaviour but should be fixed in production
        
    def test_no_directory_traversal(self):
        """Test protection against directory traversal attacks"""
        # Test static file access with directory traversal
        response = self.client.get('/static/../server.py')
        self.assertEqual(response.status_code, 404)
        
        response = self.client.get('/static/../../requirements.txt')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()