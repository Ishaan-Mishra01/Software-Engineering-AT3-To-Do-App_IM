document.addEventListener('DOMContentLoaded', function() {
    let currentList = 'All Tasks';
    let allTasks = [];

    // Load tasks on page load
    loadTasks();

    // Add task functionality
    const taskInput = document.querySelector('.task-input');
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
        taskItem.innerHTML = `
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''}>
            <span class="task-text ${task.completed ? 'completed' : ''}">${task.text}</span>
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

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: taskText,
                    list: currentList === 'All Tasks' ? 'Personal' : currentList
                })
            });

            if (response.ok) {
                const newTask = await response.json();
                allTasks.push(newTask);
                displayTasks();
                taskInput.value = '';
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
});