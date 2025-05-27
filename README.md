# To-Do App

A modern, responsive web-based To-Do application built with Flask and vanilla JavaScript, offering functionality similar to Microsoft To Do, Apple Reminders, and Google Tasks. This application demonstrates best practices in web development, including RESTful API design, responsive CSS, and modular code architecture.

![To-Do App Logo](static/To-Do_App_Logo.png)

## Table of Contents
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Project Architecture](#project-architecture)
- [Detailed File Descriptions](#detailed-file-descriptions)
- [API Documentation](#api-documentation)
- [Data Models](#data-models)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Security Considerations](#security-considerations)
- [Testing](#testing)
- [Performance Optimizations](#performance-optimizations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Features

### Core Functionality
- **User Authentication**: Secure registration and login system with session management
- **Task Management**: Full CRUD operations for tasks with real-time updates
- **Task Lists**: Organize tasks into customizable lists (Personal, Work, etc.)
- **Task States**: Mark tasks as complete/incomplete with visual feedback
- **Responsive Design**: Mobile-first design that works seamlessly across all devices
- **Clean UI**: Modern, intuitive interface with smooth transitions and animations

### Technical Features
- **RESTful API**: Well-structured API endpoints for all operations
- **Session Management**: Secure session-based authentication
- **Data Persistence**: JSON-based storage with automatic save/load
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Input Validation**: Client and server-side validation for all inputs
- **Cross-browser Compatibility**: Works on all modern browsers

## Technical Stack

### Backend
- **Framework**: Flask 2.x (Python 3.8+)
- **Session Management**: Flask-Session with secure cookies
- **Data Storage**: JSON file-based storage (easily replaceable with database)
- **API Design**: RESTful principles with proper HTTP methods

### Frontend
- **HTML5**: Semantic markup with accessibility considerations
- **CSS3**: Modern CSS with variables, flexbox, and grid
- **JavaScript**: Vanilla ES6+ with async/await and fetch API
- **Fonts**: Google Fonts (Roboto)
- **Icons**: Unicode symbols for UI elements

### Development Tools
- **Version Control**: Git with conventional commits
- **Testing**: Python unittest framework
- **Package Management**: pip with requirements.txt

## Project Architecture

```
Software-Engineering-AT3-To-Do-App_IM/
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── PROJECT_STRUCTURE.md      # Detailed project organization
├── app/                      # Flask application package
│   ├── __init__.py          # Application factory and initialization
│   ├── config.py            # Configuration settings
│   ├── routes.py            # URL routes and API endpoints
│   └── models.py            # Data models and business logic
├── static/                   # Static assets
│   ├── css/                 # Stylesheets
│   │   └── base.css         # Main stylesheet with responsive design
│   ├── js/                  # JavaScript files
│   │   └── app.js           # Frontend application logic
│   └── images/              # Image assets
│       └── To-Do_App_Logo.png
├── templates/                # Jinja2 HTML templates
│   ├── home.html            # Main application interface
│   └── login.html           # Authentication page
├── tests/                    # Comprehensive test suite
│   ├── test_unit.py         # Unit tests
│   ├── test_integration.py  # Integration tests
│   ├── test_frontend.py     # Frontend tests
│   ├── test_security.py     # Security tests
│   └── test_performance.py  # Performance tests
├── scripts/                  # Utility scripts
│   └── run_tests.py         # Test runner with coverage
└── data.json                # Local data storage (gitignored)
```

## Detailed File Descriptions

### Core Application Files

#### `run.py`
The application entry point that bootstraps the Flask application.

```python
# Key functionality:
- Imports the Flask app instance from the app package
- Configures the development server settings
- Runs the app on port 5001 with debug mode enabled
- Handles graceful shutdown on interrupt signals
```

**Usage**: `python3 run.py`

#### `requirements.txt`
Defines all Python package dependencies with version pinning for reproducibility.

```txt
Flask==2.3.2
Werkzeug==2.3.6
# Additional dependencies as needed
```

**Installation**: `pip install -r requirements.txt`

### Application Package (`app/`)

#### `app/__init__.py`
Implements the Flask application factory pattern for better testing and configuration management.

**Key Components**:
```python
- create_app() function for application initialization
- Blueprint registration for modular routing
- Session configuration with secure settings
- Error handler registration
- CORS headers setup (if needed)
```

**Features**:
- Configurable app creation for different environments
- Automatic blueprint discovery and registration
- Session lifetime and security settings
- JSON encoder customization for datetime objects

#### `app/config.py`
Centralized configuration management with environment-specific settings.

**Configuration Classes**:
```python
class Config:
    SECRET_KEY = 'your-secret-key-here'
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    DATA_FILE = 'data.json'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
```

#### `app/routes.py`
Defines all URL routes and API endpoints with proper HTTP methods and error handling.

**Route Structure**:

1. **Authentication Routes**:
   - `GET/POST /login` - User login and registration
   - `GET /logout` - Session termination
   - `GET /` - Root redirect based on auth status

2. **Page Routes**:
   - `GET /home` - Main application interface (requires auth)

3. **API Routes** (all require authentication):
   - `GET /api/tasks` - Retrieve all user tasks
   - `POST /api/tasks` - Create new task
   - `PUT /api/tasks/<task_id>` - Update existing task
   - `DELETE /api/tasks/<task_id>` - Delete task
   - `GET /api/lists` - Get user's task lists
   - `POST /api/lists` - Create new list

**Request/Response Examples**:
```python
# Create task request
POST /api/tasks
{
    "text": "Complete project documentation",
    "list": "Work",
    "due_date": "2024-12-31"
}

# Response
{
    "id": "uuid-here",
    "text": "Complete project documentation",
    "list": "Work",
    "completed": false,
    "created_at": "2024-01-20T10:30:00",
    "due_date": "2024-12-31"
}
```

#### `app/models.py`
Data models and business logic implementation with validation and error handling.

**Class Structure**:

```python
class User:
    """User model with authentication"""
    def __init__(self, email, username, password):
        self.id = str(uuid.uuid4())
        self.email = email
        self.username = username
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now()
        self.last_login = None
    
    def verify_password(self, password):
        """Verify password against hash"""
        return self.password_hash == self._hash_password(password)
    
    def to_dict(self):
        """Serialize user for storage"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Task:
    """Task model with full CRUD support"""
    def __init__(self, text, user_id, list_name="Personal"):
        self.id = str(uuid.uuid4())
        self.text = text
        self.user_id = user_id
        self.list = list_name
        self.completed = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.due_date = None
        self.priority = "normal"
    
    def update(self, **kwargs):
        """Update task attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Serialize task for API response"""
        return {
            'id': self.id,
            'text': self.text,
            'list': self.list,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date,
            'priority': self.priority
        }

class DataStore:
    """Singleton data storage manager"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.data_file = 'data.json'
        self._ensure_data_file()
    
    def save_data(self, data):
        """Atomically save data to file"""
        temp_file = f"{self.data_file}.tmp"
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        os.replace(temp_file, self.data_file)
    
    def load_data(self):
        """Load data with error recovery"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'users': [], 'tasks': []}
```

### Frontend Assets (`static/`)

#### `static/css/base.css`
Comprehensive stylesheet with modern CSS features and responsive design.

**Key Sections**:

1. **CSS Variables** (lines 10-20):
```css
:root {
    --primary-color: #2D64BD;
    --primary-hover: #4477c8;
    --text-dark: #333;
    --text-light: #666;
    --border-color: #ddd;
    --shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    --header-height: 60px;
    --sidebar-width: 250px;
    --transition-speed: 0.3s;
}
```

2. **Responsive Typography** (lines 22-37):
```css
html {
    font-size: var(--base-font-size);
}

/* Fluid typography */
h1 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
h2 { font-size: clamp(1.2rem, 3vw, 2rem); }
p { font-size: clamp(0.875rem, 2vw, 1rem); }
```

3. **Layout Components**:
   - **Login Container** (lines 50-90): Centered card with form styling
   - **Header** (lines 100-130): Fixed header with logo and navigation
   - **Sidebar** (lines 140-190): Collapsible navigation with smooth transitions
   - **Task Container** (lines 200-280): Main content area with task management

4. **Mobile Optimizations** (lines 340-465):
   - Hamburger menu for mobile navigation
   - Touch-friendly button sizes (min 44x44px)
   - Flexible layouts with wrapping
   - Optimized font sizes for readability

5. **Animations and Transitions**:
```css
.task-item {
    transition: all var(--transition-speed) ease;
}

.task-item:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow);
}

@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
```

#### `static/js/app.js`
Frontend application logic with modern JavaScript patterns.

**Core Functionality**:

1. **State Management** (lines 1-20):
```javascript
// Application state
let currentList = 'All Tasks';
let allTasks = [];
let lists = ['All Tasks', 'Personal', 'Work'];
let isLoading = false;

// Configuration
const API_BASE = '/api';
const DEBOUNCE_DELAY = 300;
```

2. **API Service Layer** (lines 30-145):
```javascript
class TaskService {
    static async getTasks() {
        try {
            const response = await fetch(`${API_BASE}/tasks`);
            if (!response.ok) throw new Error('Failed to fetch tasks');
            return await response.json();
        } catch (error) {
            console.error('Error fetching tasks:', error);
            this.showError('Failed to load tasks');
            return [];
        }
    }
    
    static async createTask(taskData) {
        try {
            const response = await fetch(`${API_BASE}/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
            if (!response.ok) throw new Error('Failed to create task');
            return await response.json();
        } catch (error) {
            console.error('Error creating task:', error);
            this.showError('Failed to create task');
            return null;
        }
    }
    
    static async updateTask(taskId, updates) {
        // Similar implementation for PUT request
    }
    
    static async deleteTask(taskId) {
        // Similar implementation for DELETE request
    }
}
```

3. **DOM Manipulation** (lines 150-300):
```javascript
class TaskUI {
    static createTaskElement(task) {
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item';
        taskItem.dataset.taskId = task.id;
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'task-checkbox';
        checkbox.checked = task.completed;
        checkbox.addEventListener('change', () => this.handleTaskToggle(task));
        
        const taskText = document.createElement('span');
        taskText.className = `task-text ${task.completed ? 'completed' : ''}`;
        taskText.textContent = task.text;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-task';
        deleteBtn.innerHTML = '×';
        deleteBtn.addEventListener('click', () => this.handleTaskDelete(task));
        
        taskItem.append(checkbox, taskText, deleteBtn);
        return taskItem;
    }
    
    static renderTasks(tasks) {
        const container = document.querySelector('.tasks');
        container.innerHTML = '';
        
        const filteredTasks = this.filterTasksByList(tasks);
        
        if (filteredTasks.length === 0) {
            container.innerHTML = '<p class="empty-state">No tasks yet. Add one above!</p>';
            return;
        }
        
        filteredTasks.forEach(task => {
            container.appendChild(this.createTaskElement(task));
        });
    }
}
```

4. **Event Handlers** (lines 310-400):
```javascript
// Debounced search
let searchTimeout;
function handleSearch(event) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const query = event.target.value.toLowerCase();
        const filtered = allTasks.filter(task => 
            task.text.toLowerCase().includes(query)
        );
        TaskUI.renderTasks(filtered);
    }, DEBOUNCE_DELAY);
}

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + N: New task
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        document.querySelector('.task-input').focus();
    }
    
    // Escape: Close mobile menu
    if (event.key === 'Escape') {
        document.querySelector('.sidebar').classList.remove('active');
    }
});
```

5. **Mobile Functionality** (lines 1-16):
```javascript
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
    
    // Trap focus when sidebar is open
    if (sidebar.classList.contains('active')) {
        sidebar.querySelector('h3').focus();
    }
}

// Touch gesture support
let touchStartX = 0;
document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
});

document.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].clientX;
    const swipeDistance = touchEndX - touchStartX;
    
    // Swipe right to open sidebar
    if (swipeDistance > 100 && touchStartX < 50) {
        document.querySelector('.sidebar').classList.add('active');
    }
    
    // Swipe left to close sidebar
    if (swipeDistance < -100) {
        document.querySelector('.sidebar').classList.remove('active');
    }
});
```

### HTML Templates (`templates/`)

#### `templates/login.html`
Responsive login/registration page with form validation and error handling.

**Key Features**:
- Combined login/register form with smart field detection
- Client-side validation with HTML5 attributes
- Server-side error message display
- Accessible form labels and ARIA attributes
- Mobile-optimized with viewport meta tag

**Form Structure**:
```html
<form method="POST" action="{{ url_for('main.login') }}" novalidate>
    <!-- Email field (required for both login and register) -->
    <div class="input-field">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" 
               placeholder="Enter your email" 
               required 
               autocomplete="email"
               pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$">
        <span class="error-message" id="email-error"></span>
    </div>
    
    <!-- Username field (only for registration) -->
    <div class="input-field">
        <label for="username">
            Username 
            <small>(only for new users)</small>
        </label>
        <input type="text" id="username" name="username" 
               placeholder="Choose a username"
               autocomplete="username"
               minlength="3"
               maxlength="20">
    </div>
    
    <!-- Password field -->
    <div class="input-field">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" 
               placeholder="Enter your password" 
               required
               autocomplete="current-password"
               minlength="6">
        <button type="button" class="toggle-password" 
                onclick="togglePasswordVisibility()">
            👁️
        </button>
    </div>
    
    <input type="submit" class="submit-button" 
           value="Login / Register">
</form>
```

#### `templates/home.html`
Main application interface with dynamic task management.

**Layout Structure**:
1. **Header Section**:
   - Logo and app title
   - User welcome message
   - Logout button
   - Mobile menu toggle

2. **Sidebar Navigation**:
   - Task list selection
   - Add new list functionality
   - Active state indication
   - Mobile-responsive behavior

3. **Main Content Area**:
   - Current list title
   - Add task form
   - Task list container
   - Empty state messaging

**Accessibility Features**:
```html
<!-- ARIA labels for screen readers -->
<nav role="navigation" aria-label="Task lists">
    <ul class="todo-lists" role="list">
        <li role="listitem" tabindex="0" 
            aria-current="page">All Tasks</li>
    </ul>
</nav>

<!-- Skip to main content link -->
<a href="#main-content" class="skip-link">
    Skip to main content
</a>

<!-- Form with proper labels -->
<form role="form" aria-label="Add new task">
    <label for="task-input" class="visually-hidden">
        New task description
    </label>
    <input type="text" id="task-input" 
           class="task-input"
           placeholder="Add a task..."
           aria-describedby="task-help">
    <span id="task-help" class="visually-hidden">
        Press Enter to add task
    </span>
</form>
```

### Testing Suite (`tests/`)

#### `tests/test_unit.py`
Comprehensive unit tests for models and utilities.

```python
import unittest
from app.models import User, Task, DataStore

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = User('test@example.com', 'testuser', 'password123')
    
    def test_user_creation(self):
        self.assertIsNotNone(self.user.id)
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertNotEqual(self.user.password_hash, 'password123')
    
    def test_password_verification(self):
        self.assertTrue(self.user.verify_password('password123'))
        self.assertFalse(self.user.verify_password('wrongpassword'))
    
    def test_user_serialization(self):
        user_dict = self.user.to_dict()
        self.assertIn('id', user_dict)
        self.assertIn('email', user_dict)
        self.assertNotIn('password', user_dict)  # Password should not be in dict

class TestTaskModel(unittest.TestCase):
    def setUp(self):
        self.task = Task('Test task', 'user123', 'Work')
    
    def test_task_defaults(self):
        self.assertFalse(self.task.completed)
        self.assertEqual(self.task.priority, 'normal')
        self.assertIsNone(self.task.due_date)
    
    def test_task_update(self):
        self.task.update(completed=True, priority='high')
        self.assertTrue(self.task.completed)
        self.assertEqual(self.task.priority, 'high')
        self.assertGreater(self.task.updated_at, self.task.created_at)
```

#### `tests/test_integration.py`
Integration tests for API endpoints.

```python
import unittest
import json
from app import create_app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create test user and login
        self.register_and_login()
    
    def tearDown(self):
        self.app_context.pop()
    
    def register_and_login(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_get_tasks_empty(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 0)
    
    def test_create_task(self):
        response = self.client.post('/api/tasks',
            data=json.dumps({'text': 'New task', 'list': 'Personal'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        task = json.loads(response.data)
        self.assertEqual(task['text'], 'New task')
        self.assertFalse(task['completed'])
    
    def test_update_task(self):
        # First create a task
        create_response = self.client.post('/api/tasks',
            data=json.dumps({'text': 'Task to update'}),
            content_type='application/json'
        )
        task = json.loads(create_response.data)
        
        # Update the task
        update_response = self.client.put(f'/api/tasks/{task["id"]}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        self.assertEqual(update_response.status_code, 200)
        updated_task = json.loads(update_response.data)
        self.assertTrue(updated_task['completed'])
```

#### `tests/test_security.py`
Security-focused tests for authentication and authorization.

```python
class TestSecurity(unittest.TestCase):
    def test_unauthorized_access(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_session_expiry(self):
        # Login
        self.register_and_login()
        
        # Access protected route
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        
        # Clear session
        with self.client.session_transaction() as sess:
            sess.clear()
        
        # Try to access protected route again
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)
    
    def test_sql_injection_prevention(self):
        # Attempt SQL injection in login
        response = self.client.post('/login', data={
            'email': "test@example.com'; DROP TABLE users; --",
            'password': 'password'
        })
        # Should fail gracefully without executing SQL
        self.assertIn(b'Invalid credentials', response.data)
    
    def test_xss_prevention(self):
        # Login first
        self.register_and_login()
        
        # Try to create task with XSS payload
        response = self.client.post('/api/tasks',
            data=json.dumps({
                'text': '<script>alert("XSS")</script>',
                'list': 'Personal'
            }),
            content_type='application/json'
        )
        task = json.loads(response.data)
        # Script tags should be escaped
        self.assertNotIn('<script>', task['text'])
```

## API Documentation

### Authentication Endpoints

#### POST /login
Authenticate existing user or register new user.

**Request Body**:
```json
{
    "email": "user@example.com",
    "password": "securepassword",
    "username": "newuser"  // Optional, only for registration
}
```

**Response**:
- Success: 302 redirect to /home
- Failure: 200 with error message

#### GET /logout
Terminate user session.

**Response**: 302 redirect to /login

### Task Management Endpoints

#### GET /api/tasks
Retrieve all tasks for authenticated user.

**Query Parameters**:
- `list` (optional): Filter by list name
- `completed` (optional): Filter by completion status

**Response**: 200 OK
```json
[
    {
        "id": "uuid",
        "text": "Task description",
        "list": "Personal",
        "completed": false,
        "created_at": "2024-01-20T10:30:00",
        "updated_at": "2024-01-20T10:30:00",
        "due_date": null,
        "priority": "normal"
    }
]
```

#### POST /api/tasks
Create new task.

**Request Body**:
```json
{
    "text": "Task description",
    "list": "Work",
    "due_date": "2024-12-31",
    "priority": "high"
}
```

**Response**: 201 Created
```json
{
    "id": "new-uuid",
    "text": "Task description",
    "list": "Work",
    "completed": false,
    "created_at": "2024-01-20T10:30:00",
    "updated_at": "2024-01-20T10:30:00",
    "due_date": "2024-12-31",
    "priority": "high"
}
```

#### PUT /api/tasks/{task_id}
Update existing task.

**Request Body** (all fields optional):
```json
{
    "text": "Updated description",
    "completed": true,
    "list": "Personal",
    "due_date": "2024-12-31",
    "priority": "low"
}
```

**Response**: 200 OK with updated task object

#### DELETE /api/tasks/{task_id}
Delete task.

**Response**: 204 No Content

## Data Models

### User Schema
```json
{
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "password_hash": "hashed_password",
    "created_at": "2024-01-20T10:30:00",
    "last_login": "2024-01-20T15:45:00"
}
```

### Task Schema
```json
{
    "id": "uuid",
    "user_id": "user-uuid",
    "text": "Task description",
    "list": "Personal",
    "completed": false,
    "created_at": "2024-01-20T10:30:00",
    "updated_at": "2024-01-20T10:30:00",
    "due_date": "2024-12-31",
    "priority": "normal"
}
```

### Storage Format (data.json)
```json
{
    "users": [
        {
            "id": "user1-uuid",
            "email": "user@example.com",
            "username": "user1",
            "password_hash": "hashed_password",
            "created_at": "2024-01-20T10:30:00",
            "last_login": "2024-01-20T15:45:00"
        }
    ],
    "tasks": [
        {
            "id": "task1-uuid",
            "user_id": "user1-uuid",
            "text": "Complete project",
            "list": "Work",
            "completed": false,
            "created_at": "2024-01-20T10:30:00",
            "updated_at": "2024-01-20T10:30:00",
            "due_date": null,
            "priority": "high"
        }
    ]
}
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for version control)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Software-Engineering-AT3-To-Do-App_IM
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python3 run.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5001`

### Configuration Options

You can customize the application by modifying `app/config.py`:

```python
# Change port
PORT = 5001

# Change secret key (use environment variable in production)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Change data file location
DATA_FILE = os.path.join(BASE_DIR, 'data', 'tasks.json')

# Session timeout (in seconds)
PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
```

## Usage Guide

### First Time Setup
1. Navigate to `http://localhost:5001`
2. You'll be redirected to the login page
3. Fill in all fields (email, username, password) to register
4. You'll be automatically logged in after successful registration

### Daily Usage

#### Adding Tasks
1. Type your task in the input field at the top
2. Press Enter or click "Add" button
3. Task appears immediately in the list below

#### Managing Tasks
- **Complete**: Click the checkbox next to a task
- **Delete**: Click the × button on the right
- **Edit**: Double-click task text (future feature)

#### Organizing with Lists
1. Click on different lists in the sidebar
2. Tasks are automatically filtered by list
3. New tasks are added to the currently selected list

#### Keyboard Shortcuts
- `Ctrl/Cmd + N`: Focus on new task input
- `Enter`: Add task (when input is focused)
- `Escape`: Close mobile menu
- `Tab`: Navigate through interface elements

### Mobile Usage
- Tap the ☰ menu icon to open sidebar
- Swipe right from left edge to open sidebar
- Swipe left to close sidebar
- All features work with touch interactions

## Security Considerations

### Current Security Measures
1. **Session Management**: Secure session cookies with httponly flag
2. **Password Storage**: Passwords are hashed (upgrade to bcrypt recommended)
3. **Input Validation**: Both client and server-side validation
4. **XSS Prevention**: All user input is escaped before display
5. **CSRF Protection**: Should be added for production

### Recommended Production Enhancements
1. **Use HTTPS**: Essential for secure data transmission
2. **Implement bcrypt**: For secure password hashing
3. **Add CSRF tokens**: Prevent cross-site request forgery
4. **Rate limiting**: Prevent brute force attacks
5. **SQL injection prevention**: When migrating to database
6. **Content Security Policy**: Add CSP headers
7. **Secure headers**: X-Frame-Options, X-Content-Type-Options

### Example Security Implementation
```python
# In app/__init__.py
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_wtf.csrf import CSRFProtect

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
limiter = Limiter(
    app,
    key_func=lambda: session.get('user_id', request.remote_addr),
    default_limits=["200 per day", "50 per hour"]
)

# In routes.py
@limiter.limit("5 per minute")
@app.route('/login', methods=['POST'])
def login():
    # Login logic
```

## Testing

### Running Tests
```bash
# Run all tests
python scripts/run_tests.py

# Run specific test file
python -m unittest tests.test_unit

# Run with coverage
python -m coverage run -m unittest discover tests
python -m coverage report
```

### Test Coverage
- **Unit Tests**: Models, utilities, helpers
- **Integration Tests**: API endpoints, database operations
- **Frontend Tests**: JavaScript functions, DOM manipulation
- **Security Tests**: Authentication, authorization, input validation
- **Performance Tests**: Load testing, response times

### Writing New Tests
```python
# Example test structure
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up code
    
    def test_feature_behavior(self):
        """Test specific behavior"""
        # Arrange
        test_data = {'key': 'value'}
        
        # Act
        result = function_under_test(test_data)
        
        # Assert
        self.assertEqual(result, expected_value)
```

## Performance Optimizations

### Current Optimizations
1. **Efficient DOM Updates**: Only update changed elements
2. **Debounced Search**: Prevent excessive API calls
3. **Lazy Loading**: Load tasks on demand
4. **CSS Animations**: Hardware-accelerated transitions
5. **Minified Assets**: Reduced file sizes for production

### Recommended Optimizations
1. **Database Indexing**: When migrating from JSON
2. **Caching**: Redis for session and data caching
3. **CDN**: Serve static assets from CDN
4. **Compression**: Gzip responses
5. **Bundle Optimization**: Webpack for asset bundling

### Performance Monitoring
```python
# Add performance logging
import time
from functools import wraps

def measure_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        app.logger.info(f'{f.__name__} took {end_time - start_time:.3f}s')
        return result
    return decorated_function

@app.route('/api/tasks')
@measure_performance
def get_tasks():
    # Route logic
```

## Future Enhancements

### Planned Features
1. **Custom Lists**: Create, rename, and delete custom lists
2. **Due Dates**: Set and track task deadlines
3. **Reminders**: Email/push notifications for due tasks
4. **Tags**: Categorize tasks with colored tags
5. **Search**: Full-text search across all tasks
6. **Sharing**: Share lists with other users
7. **Themes**: Dark mode and custom color themes
8. **Export**: Download tasks as CSV/JSON
9. **Mobile Apps**: Native iOS/Android applications
10. **Offline Support**: Service workers for offline functionality

### Technical Improvements
1. **Database Migration**: PostgreSQL for scalability
2. **API Versioning**: Support multiple API versions
3. **WebSockets**: Real-time updates across devices
4. **Microservices**: Separate services for auth, tasks, notifications
5. **Container Deployment**: Docker and Kubernetes support
6. **CI/CD Pipeline**: Automated testing and deployment
7. **Monitoring**: Application performance monitoring
8. **Analytics**: User behavior tracking (with consent)

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes following code style guidelines
4. Write tests for new functionality
5. Ensure all tests pass (`python scripts/run_tests.py`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open Pull Request

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Write self-documenting code
- Add comments for complex logic

### Commit Message Format
```
type(scope): subject

body

footer
```

Example:
```
feat(tasks): add due date functionality

- Add due_date field to Task model
- Update API to handle due dates
- Add date picker to frontend

Closes #123
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation and community
- Google Fonts for Roboto typeface
- Contributors and testers
- Inspired by Microsoft To Do, Apple Reminders, and Google Tasks