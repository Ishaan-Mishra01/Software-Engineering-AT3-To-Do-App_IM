// Mobile menu toggle function
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    
    if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
        !sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
        sidebar.classList.remove('active');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    let currentList = 'All Tasks';
    let allTasks = [];

    // Load tasks on page load
    loadTasks();

    // Add task functionality
    const taskInput = document.querySelector('.task-input');
    const dueDateInput = document.querySelector('.due-date-input');
    const addTaskBtn = document.querySelector('.add-task-btn');

    addTaskBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    // List selection
    document.querySelectorAll('.list-item').forEach(item => {
        item.addEventListener('click', function() {
            document.querySelector('.list-item.active').classList.remove('active');
            this.classList.add('active');
            currentList = this.textContent;
            document.querySelector('.todo-container h2').textContent = currentList;
            displayTasks();
        });
    });

    // Load tasks from server
    async function loadTasks() {
        try {
            const response = await fetch('/api/tasks');
            if (response.ok) {
                allTasks = await response.json();
                displayTasks();
            }
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    // Display tasks based on current list
    function displayTasks() {
        const tasksContainer = document.querySelector('.tasks');
        tasksContainer.innerHTML = '';

        const filteredTasks = currentList === 'All Tasks' 
            ? allTasks 
            : allTasks.filter(task => task.list === currentList);

        filteredTasks.forEach(task => {
            const taskElement = createTaskElement(task);
            tasksContainer.appendChild(taskElement);
        });
    }

    // Create task element
    function createTaskElement(task) {
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item';
        const dueDateDisplay = task.due_date ? `<span class="due-date">Due: ${task.due_date}</span>` : '';
        taskItem.innerHTML = `
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''}>
            <span class="task-text ${task.completed ? 'completed' : ''}">${task.text}</span>
            ${dueDateDisplay}
            <button class="delete-task">×</button>
        `;

        // Toggle task completion
        taskItem.querySelector('.task-checkbox').addEventListener('change', async function() {
            task.completed = this.checked;
            taskItem.querySelector('.task-text').classList.toggle('completed');
            await updateTask(task.id, { completed: task.completed });
        });

        // Delete task
        taskItem.querySelector('.delete-task').addEventListener('click', async function() {
            await deleteTask(task.id);
            allTasks = allTasks.filter(t => t.id !== task.id);
            displayTasks();
        });

        return taskItem;
    }

    // Add new task
    async function addTask() {
        const taskText = taskInput.value.trim();
        if (!taskText) return;

        const dueDate = dueDateInput.value;

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: taskText,
                    list: currentList === 'All Tasks' ? 'Personal' : currentList,
                    due_date: dueDate || null
                })
            });

            if (response.ok) {
                const newTask = await response.json();
                allTasks.push(newTask);
                displayTasks();
                taskInput.value = '';
                dueDateInput.value = '';
            }
        } catch (error) {
            console.error('Error adding task:', error);
        }
    }

    // Update task
    async function updateTask(taskId, updates) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updates)
            });

            if (!response.ok) {
                console.error('Error updating task');
            }
        } catch (error) {
            console.error('Error updating task:', error);
        }
    }

    // Delete task
    async function deleteTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                console.error('Error deleting task');
            }
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    }

    // Chatbot functionality
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotMessages = document.getElementById('chatbot-messages');

    let chatbotOpen = false;

    // Toggle chatbot
    chatbotToggle.addEventListener('click', function() {
        chatbotOpen = !chatbotOpen;
        chatbotContainer.style.display = chatbotOpen ? 'flex' : 'none';
        chatbotToggle.style.display = chatbotOpen ? 'none' : 'block';
        
        if (chatbotOpen && chatbotMessages.children.length === 0) {
            // Add welcome message
            addChatMessage('🤖 Hi! I\'m here to help you with your to-do app. Ask me anything!', 'bot');
        }
    });

    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotOpen = false;
        chatbotContainer.style.display = 'none';
        chatbotToggle.style.display = 'block';
    });

    // Send message
    chatbotSend.addEventListener('click', sendChatMessage);
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });

    async function sendChatMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        // Add user message
        addChatMessage(message, 'user');
        chatbotInput.value = '';

        try {
            const response = await fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (response.ok) {
                const data = await response.json();
                addChatMessage(data.message, 'bot');
            } else {
                addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            addChatMessage('Sorry, I\'m having trouble connecting. Please try again.', 'bot');
        }
    }

    function addChatMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender}`;
        messageElement.innerHTML = `
            <div class="message-content">
                ${message.replace(/\n/g, '<br>')}
            </div>
        `;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
});