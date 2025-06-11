
"""
Chatbot functionality for To-Do Application
"""
import os
from flask import session, has_request_context
from app.models import load_data

# For now, we'll implement a simple rule-based chatbot
# Later this can be extended with actual AI integration

def get_chatbot_response(user_message):
    """Get response from chatbot based on user message"""
    message = user_message.lower().strip()
    
    # Task management queries
    if any(word in message for word in ['create', 'add', 'new task']):
        return {
            'response': "To create a new task:\n1. Type your task in the input field at the top\n2. Optionally select a due date\n3. Click 'Add' or press Enter\n\nYou can also organize tasks into different lists like Personal or Work!",
            'type': 'task_help'
        }
    
    elif any(word in message for word in ['delete', 'remove', 'complete']):
        return {
            'response': "To manage tasks:\n• Check the checkbox to mark as complete\n• Click the × button to delete a task\n• Completed tasks over 30 days old are automatically deleted\n\nYou can view completed tasks in the 'All Tasks' view.",
            'type': 'task_help'
        }
    
    elif any(word in message for word in ['cleanup', 'clean up', 'remove old', 'delete old']):
        return {
            'response': "I can help clean up old completed tasks! Tasks that have been completed for more than 30 days are automatically removed. If you'd like to manually trigger this cleanup, I can do that for you.\n\nWould you like me to clean up old completed tasks now?",
            'type': 'cleanup_offer'
        }
    
    elif any(word in message for word in ['show', 'list', 'current tasks', 'all tasks']):
        # Get user's current tasks
        if has_request_context() and 'email' in session:
            data = load_data()
            user_tasks = data['tasks'].get(session['email'], [])
            active_tasks = [t for t in user_tasks if not t['completed']]
            completed_tasks = [t for t in user_tasks if t['completed']]
            
            response = f"You currently have:\n• {len(active_tasks)} active tasks\n• {len(completed_tasks)} completed tasks\n\n"
            
            if active_tasks:
                response += "Active tasks:\n"
                for task in active_tasks[:5]:  # Show first 5
                    due_info = f" (Due: {task['due_date']})" if task.get('due_date') else ""
                    response += f"• {task['text']}{due_info}\n"
                if len(active_tasks) > 5:
                    response += f"... and {len(active_tasks) - 5} more"
            
            return {'response': response, 'type': 'task_list'}
        else:
            return {'response': "I can help you view your tasks when you're logged in! Your current tasks will be displayed here with their due dates and completion status.", 'type': 'info'}
    
    # Personalization queries
    elif any(word in message for word in ['theme', 'personalize', 'customize', 'settings']):
        return {
            'response': "Personalization features:\n• Different task lists (Personal, Work, etc.)\n• Calendar view for due dates\n• Task organization and filtering\n\nMore customization options are coming soon!",
            'type': 'personalization'
        }
    
    # Calendar queries
    elif any(word in message for word in ['calendar', 'due date', 'schedule']):
        return {
            'response': "Calendar features:\n• Click 'Calendar' in the sidebar to view your tasks by date\n• Add due dates when creating tasks\n• See all tasks organized by their due dates\n• Navigate between months to plan ahead",
            'type': 'calendar_help'
        }
    
    # General app help
    elif any(word in message for word in ['help', 'how to', 'tutorial']):
        return {
            'response': "Welcome to your To-Do App! Here's what you can do:\n\n📝 Manage Tasks:\n• Add new tasks with due dates\n• Mark tasks as complete\n• Delete tasks you no longer need\n\n📅 Calendar View:\n• See tasks organized by due date\n• Plan your schedule visually\n\n📋 Lists:\n• Organize tasks into different categories\n• Switch between Personal, Work, etc.\n\nAsk me anything specific!",
            'type': 'general_help'
        }
    
    # Default response
    else:
        return {
            'response': "I'm here to help with your To-Do app! You can ask me about:\n• How to create or delete tasks\n• Using the calendar feature\n• Organizing your tasks\n• App features and settings\n\nWhat would you like to know?",
            'type': 'default'
        }

def format_chatbot_response(response_data):
    """Format the chatbot response for display"""
    return {
        'message': response_data['response'],
        'type': response_data['type'],
        'timestamp': None  # Can add timestamp if needed
    }