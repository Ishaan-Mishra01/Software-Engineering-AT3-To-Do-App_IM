# To-Do App

A web-based To-Do application built with Flask and vanilla JavaScript, offering functionality similar to Microsoft To Do, Apple Reminders, and Google Tasks.

![To-Do App Logo](static/To-Do_App_Logo.png)

## Features

- **User Authentication**: Register and login with email/password
- **Task Management**: Create, update, delete, and mark tasks as complete
- **Task Lists**: Organise tasks into different lists (Personal, Work, etc.)
- **Responsive Design**: Works well on desktop and mobile devices
- **Clean UI**: Modern, intuitive interface with smooth interactions

## Project Structure

```
Software-Engineering-AT3-To-Do-App_IM/
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
├── app/                  # Flask application package
│   ├── __init__.py      # Application factory
│   ├── config.py        # Configuration settings
│   ├── routes.py        # URL routes and views
│   └── models.py        # Data models and storage
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   │   └── base.css    # Main stylesheet
│   ├── js/             # JavaScript files
│   │   └── app.js      # Frontend functionality
│   └── images/         # Images and logos
│       └── To-Do_App_Logo.png
├── templates/           # HTML templates
│   ├── home.html       # Main To-Do interface
│   └── login.html      # Login/Register page
├── tests/              # Test suite
│   └── ...             # Various test files
├── scripts/            # Utility scripts
│   └── run_tests.py    # Test runner
└── data.json           # Local data storage (gitignored)
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Software-Engineering-AT3-To-Do-App_IM
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python3 run.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5001`

## Usage

1. **First Time Users**: 
   - Go to the login page
   - Fill in all fields (email, username, password) to register
   - You'll be automatically logged in after registration

2. **Returning Users**:
   - Enter your email and password only
   - Leave the username field empty

3. **Managing Tasks**:
   - Add tasks using the input field
   - Click checkboxes to mark tasks as complete
   - Click the × button to delete tasks
   - Switch between different lists in the sidebar

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Data Storage**: JSON file (for demo purposes)
- **Authentication**: Session-based
- **API**: RESTful endpoints for task management

## Security Note

This is a demonstration project. For production use:
- Replace file-based storage with a proper database
- Implement proper password hashing
- Use environment variables for sensitive configuration
- Add CSRF protection
- Implement rate limiting

## Future Enhancements

- Add ability to create custom lists
- Implement due dates and reminders
- Add task priorities and tags
- Enable task sharing between users
- Add drag-and-drop functionality
- Implement data export/import features