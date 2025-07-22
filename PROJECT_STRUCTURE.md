# Project Structure

```
Software-Engineering-AT3-To-Do-App_IM/
│
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── PROJECT_STRUCTURE.md    # This file
├── .gitignore              # Git ignore rules
├── .env.example            # Environment variables example
│
├── app/                    # Flask application package
│   ├── __init__.py        # Application factory
│   ├── config.py          # Configuration settings
│   ├── routes.py          # URL routes and view functions
│   ├── models.py          # Data models and storage
│   └── README.md          # App package documentation
│
├── static/                 # Static assets (CSS, JS, images)
│   ├── css/
│   │   ├── base.css       # Main stylesheet
│   │   └── README.md      # CSS documentation
│   ├── js/
│   │   ├── app.js         # Frontend JavaScript
│   │   └── README.md      # JS documentation
│   └── images/
│       └── To-Do_App_Logo.png
│
├── templates/              # HTML templates
│   ├── home.html          # Main application page
│   └── login.html         # Login/Registration page
│
├── tests/                  # All test files
│   ├── __init__.py        # Test package marker
│   ├── test_unit.py       # Unit tests
│   ├── test_integration.py # Integration tests
│   ├── test_frontend.py   # Frontend tests
│   ├── test_security.py   # Security tests
│   ├── test_performance.py # Performance tests
│   ├── test_app.py        # API tests
│   ├── test_ui.html       # Manual UI test page
│   ├── README.md          # Test documentation
│   ├── TEST_RESULTS.md    # Test results
│   └── TESTING_COMPLETE.md # Testing summary
│
├── scripts/                # Utility scripts
│   ├── run_tests.py       # Master test runner
│   └── README.md          # Scripts documentation
│
├── data.json              # Local data storage (gitignored)
└── server.log             # Server logs (gitignored)
```

## Directory Purposes

### `/app`
Core Flask application code:
- Application factory pattern
- Route definitions
- Data models
- Configuration management

### `/static`
Contains all static assets served directly by the web server:
- **css/**: Stylesheets
- **js/**: JavaScript files
- **images/**: Images and icons

### `/templates`
Contains Jinja2 HTML templates rendered by Flask

### `/tests`
Contains all test files and testing documentation

### `/scripts`
Utility scripts for development and testing

### Root Directory
Contains:
- Application entry point (`run.py`)
- Configuration files
- Documentation
- Environment setup