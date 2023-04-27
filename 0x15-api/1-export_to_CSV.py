#!/usr/bin/python3
import csv
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
employee_username = user_data['username']

# Make a request to the API to get the todo list information for the employee
todo_url = base_url + 'todos?userId={}'.format(employee_id)
todo_response = requests.get(todo_url)

# Parse the todo list information
todo_data = todo_response.json()
tasks = []

# Find the number of completed tasks and the titles of those tasks
for task in todo_data:
    task_completed_status = "COMPLETED" if task['completed'] else "INCOMPLETE"
    task_title = task['title']
    tasks.append([employee_id, employee_username, task_completed_status, task_title])

# Write the employee's tasks to a CSV file
with open('{}.csv'.format(employee_id), mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['USER_ID', 'USERNAME', 'TASK_COMPLETED_STATUS', 'TASK_TITLE'])
    writer.writerows(tasks)

# Print the employee's progress report
print("Employee {} is done with tasks({}/{}):".format(employee_name, len([t for t in tasks if t[2] == "COMPLETED"]), len(tasks)))
for task in tasks:
    if task[2] == "COMPLETED":
        print("\t{}".format(task[3]))

