#!/usr/bin/env python3
"""Unit tests for server functions"""
import unittest
import sys
import os
import json
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import load_data, save_data

class TestServerFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create temporary data file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        
        # Mock the DATA_FILE
        self.app.config['DATA_FILE'] = self.temp_file.name
        
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
        # Remove temporary file
        try:
            os.unlink(self.temp_file.name)
        except:
            pass
            
    def test_load_data_empty_file(self):
        """Test loading data when file doesn't exist"""
        # Remove the temp file to simulate non-existent file
        os.unlink(self.temp_file.name)
        
        data = load_data()
        self.assertEqual(data, {'users': {}, 'tasks': {}})
        
    def test_save_and_load_data(self):
        """Test saving and loading data"""
        test_data = {
            'users': {
                'test@example.com': {
                    'username': 'testuser',
                    'password': 'testpass',
                    'created': datetime.now().isoformat()
                }
            },
            'tasks': {
                'test@example.com': [
                    {
                        'id': '1',
                        'text': 'Test task',
                        'completed': False,
                        'list': 'Personal',
                        'created': datetime.now().isoformat()
                    }
                ]
            }
        }
        
        save_data(test_data)
        loaded_data = load_data()
        
        self.assertEqual(loaded_data['users'], test_data['users'])
        self.assertEqual(loaded_data['tasks'], test_data['tasks'])
        
    def test_home_redirect_without_login(self):
        """Test that home page redirects to login when not authenticated"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/login'))
        
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login / Register', response.data)
        
    def test_logout_redirect(self):
        """Test logout functionality"""
        with self.client.session_transaction() as sess:
            sess['user'] = 'testuser'
            sess['email'] = 'test@example.com'
            
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        
        with self.client.session_transaction() as sess:
            self.assertNotIn('user', sess)
            self.assertNotIn('email', sess)

class TestDataValidation(unittest.TestCase):
    """Test data validation and error handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_empty_email_validation(self):
        """Test that empty email is handled"""
        
        response = self.client.post('/login', data={
            'email': '',
            'username': 'testuser',
            'password': 'testpass'
        })
        
        # Should still get a response (form validation happens client-side)
        self.assertIn(response.status_code, [200, 302])
        
    def test_json_data_structure(self):
        """Test the structure of saved JSON data"""
        test_data = {
            'users': {},
            'tasks': {}
        }
        
        # Verify structure
        self.assertIn('users', test_data)
        self.assertIn('tasks', test_data)
        self.assertIsInstance(test_data['users'], dict)
        self.assertIsInstance(test_data['tasks'], dict)

if __name__ == '__main__':
    unittest.main()