#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_server_running():
    try:
        response = requests.get(BASE_URL)
        print("✅ Server is running")
        return True
    except:
        print("❌ Server is not running")
        return False

def test_registration():
    print("\n=== Testing Registration ===")
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:  # Redirect after successful registration
        print("✅ Registration successful")
        return True
    else:
        print(f"❌ Registration failed: {response.status_code}")
        return False

def test_login():
    print("\n=== Testing Login ===")
    session = requests.Session()
    
    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = session.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        print("✅ Login successful")
        return session
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None

def test_tasks_api(session):
    print("\n=== Testing Tasks API ===")
    
    # Test creating a task
    print("Testing task creation...")
    task_data = {
        'text': 'Test task from automated test',
        'list': 'Personal'
    }
    
    response = session.post(f"{BASE_URL}/api/tasks", 
                           json=task_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        task = response.json()
        print(f"✅ Task created with ID: {task['id']}")
        task_id = task['id']
    else:
        print(f"❌ Task creation failed: {response.status_code}")
        return False
    
    # Test getting tasks
    print("\nTesting task retrieval...")
    response = session.get(f"{BASE_URL}/api/tasks")
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Retrieved {len(tasks)} task(s)")
    else:
        print(f"❌ Task retrieval failed: {response.status_code}")
        return False
    
    # Test updating a task
    print("\nTesting task update...")
    update_data = {'completed': True}
    response = session.put(f"{BASE_URL}/api/tasks/{task_id}", 
                          json=update_data,
                          headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        print("✅ Task updated successfully")
    else:
        print(f"❌ Task update failed: {response.status_code}")
        return False
    
    # Test deleting a task
    print("\nTesting task deletion...")
    response = session.delete(f"{BASE_URL}/api/tasks/{task_id}")
    if response.status_code == 200:
        print("✅ Task deleted successfully")
    else:
        print(f"❌ Task deletion failed: {response.status_code}")
        return False
    
    return True

def test_logout(session):
    print("\n=== Testing Logout ===")
    response = session.get(f"{BASE_URL}/logout", allow_redirects=False)
    if response.status_code == 302:
        print("✅ Logout successful")
        return True
    else:
        print(f"❌ Logout failed: {response.status_code}")
        return False

def main():
    print("Starting To-Do App Tests...")
    
    if not test_server_running():
        print("\nPlease start the Flask server first with: python3 server.py")
        return
    
    time.sleep(1)
    
    # Run tests
    test_registration()
    session = test_login()
    
    if session:
        test_tasks_api(session)
        test_logout(session)
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()