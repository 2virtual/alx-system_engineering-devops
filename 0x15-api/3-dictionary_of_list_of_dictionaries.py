#!/usr/bin/python3
# script to gather all todo data from an API and write to JSON file
import json
import requests
import sys

# Check if the employee ID was provided as a parameter
if len(sys.argv) != 2:
    print("Usage: {} EMPLOYEE_ID".format(sys.argv[0]))
    sys.exit(1)

# Base URL of the API
base_url = 'https://jsonplaceholder.typicode.com/'

# Get the employee ID from the command line arguments
employee_id = sys.argv[1]

# Make a request to the API to get the user information
user_url = base_url + 'users/{}'.format(employee_id)
user_response = requests.get(user_url)

# Check if the user exists
if user_response.status_code != 200:
    print("Error: Employee with ID {} not found.".format(employee_id))
    sys.exit(1)

# Parse the user information
user_data = user_response.json()
employee_name = user_data['name']

# Make a request to the API to get the todo list information for the employee
todo_url = base_url + 'todos?userId={}'.format(employee_id)
todo_response = requests.get(todo_url)

# Parse the todo list information
todo_data = todo_response.json()
tasks = []

# Find the number of completed tasks and the titles of those tasks
for task in todo_data:
    tasks.append({
        "username": employee_name,
        "task": task['title'],
        "completed": task['completed']
    })

# Print the employee's progress report
print("Employee {} is done with tasks({}/{}):".format(employee_name, len([t for t in tasks if t['completed']]), len(tasks)))

# Export data in JSON format for all employees
all_tasks = {}
for user_id in range(1, 11):
    user_url = base_url + 'users/{}'.format(user_id)
    user_response = requests.get(user_url)
    if user_response.status_code == 200:
        user_data = user_response.json()
        employee_name = user_data['name']
        todo_url = base_url + 'todos?userId={}'.format(user_id)
        todo_response = requests.get(todo_url)
        todo_data = todo_response.json()
        tasks = []
        for task in todo_data:
            tasks.append({
                "username": employee_name,
                "task": task['title'],
                "completed": task['completed']
            })
        all_tasks[str(user_id)] = tasks

# Write the data to a JSON file
with open('todo_all_employees.json', 'w') as f:
    json.dump(all_tasks, f)

