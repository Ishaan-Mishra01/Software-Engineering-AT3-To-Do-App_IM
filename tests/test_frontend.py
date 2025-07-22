#!/usr/bin/env python3
"""Frontend tests - testing HTML/CSS/JS rendering and functionality"""
import unittest
import sys
import os
import re

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestFrontendRendering(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
    def test_login_page_elements(self):
        """Test that login page contains all required elements"""
        response = self.client.get('/login')
        html = response.data.decode('utf-8')
        
        # Check for form elements
        self.assertIn('<form method="POST"', html)
        self.assertIn('name="email"', html)
        self.assertIn('name="username"', html)
        self.assertIn('name="password"', html)
        self.assertIn('type="submit"', html)
        
        # Check for labels
        self.assertIn('Email', html)
        self.assertIn('Username', html)
        self.assertIn('Password', html)
        
        # Check for logo
        self.assertIn('To-Do_App_Logo.png', html)
        
        # Check for CSS and fonts
        self.assertIn('base.css', html)
        self.assertIn('fonts.googleapis.com', html)
        
    def test_home_page_authenticated(self):
        """Test home page rendering when authenticated"""
        # Register and login
        register_data = {
            'email': 'frontend@test.com',
            'username': 'frontendtest',
            'password': 'testpass'
        }
        self.client.post('/login', data=register_data)
        
        # Get home page
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        
        # Check for main elements
        self.assertIn('Welcome, frontendtest!', html)
        self.assertIn('Logout', html)
        self.assertIn('All Tasks', html)
        self.assertIn('Personal', html)
        self.assertIn('Work', html)
        self.assertIn('Add a task...', html)
        
        # Check for JavaScript
        self.assertIn('app.js', html)
        
        # Check for task container
        self.assertIn('class="todo-container"', html)
        self.assertIn('class="sidebar"', html)
        
    def test_static_files_exist(self):
        """Test that static files are accessible"""
        # Test CSS
        response = self.client.get('/static/css/base.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response.content_type)
        
        # Test JavaScript
        response = self.client.get('/static/js/app.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn('javascript', response.content_type)
        
    def test_css_content(self):
        """Test CSS file contains expected styles"""
        response = self.client.get('/static/css/base.css')
        css = response.data.decode('utf-8')
        
        # Check for key styles
        self.assertIn('.login-form-container', css)
        self.assertIn('.todo-container', css)
        self.assertIn('.task-item', css)
        self.assertIn('.sidebar', css)
        
        # Check for responsive design
        self.assertIn('@media', css)
        
        # Check that CSS uses standard color property (which is correct in CSS)
        # Note: 'color' is a CSS property and should not be changed to 'colour'
        self.assertIn('color:', css)
        
    def test_javascript_content(self):
        """Test JavaScript file contains expected functions"""
        response = self.client.get('/static/js/app.js')
        js = response.data.decode('utf-8')
        
        # Check for key functions
        self.assertIn('loadTasks', js)
        self.assertIn('addTask', js)
        self.assertIn('deleteTask', js)
        self.assertIn('updateTask', js)
        self.assertIn('displayTasks', js)
        
        # Check for API calls
        self.assertIn('/api/tasks', js)
        self.assertIn('fetch', js)
        
        # Check for event listeners
        self.assertIn('addEventListener', js)
        self.assertIn('DOMContentLoaded', js)
        
    def test_error_message_display(self):
        """Test error message display on login failure"""
        # First register a user
        register_data = {
            'email': 'error@test.com',
            'username': 'errortest',
            'password': 'correctpass'
        }
        self.client.post('/login', data=register_data)
        self.client.get('/logout')
        
        # Try to login with wrong password
        login_data = {
            'email': 'error@test.com',
            'password': 'wrongpass'
        }
        
        response = self.client.post('/login', data=login_data)
        html = response.data.decode('utf-8')
        
        # Check for error message
        self.assertIn('Invalid credentials', html)
        self.assertIn('color: red', html)
        
    def test_form_validation_attributes(self):
        """Test HTML5 form validation attributes"""
        response = self.client.get('/login')
        html = response.data.decode('utf-8')
        
        # Check for required attributes
        email_input = re.search(r'<input[^>]*name="email"[^>]*>', html)
        self.assertIsNotNone(email_input)
        self.assertIn('required', email_input.group())
        self.assertIn('type="email"', email_input.group())
        
        password_input = re.search(r'<input[^>]*name="password"[^>]*>', html)
        self.assertIsNotNone(password_input)
        self.assertIn('required', password_input.group())
        self.assertIn('type="password"', password_input.group())
        
    def test_responsive_meta_tag(self):
        """Test responsive design meta tag"""
        response = self.client.get('/login')
        html = response.data.decode('utf-8')
        
        self.assertIn('viewport', html)
        self.assertIn('width=device-width', html)
        self.assertIn('initial-scale=1.0', html)

    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()