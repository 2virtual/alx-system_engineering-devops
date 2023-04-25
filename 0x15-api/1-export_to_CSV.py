#!/usr/bin/python3
# script to gather todo data from an API and write to CSV file
import csv
import requests
import sys

# Check if the employee ID was provided as a parameter
if len(sys.argv) != 2:
    print("Usage: {} EMPLOYEE_ID".format(sys.argv[0]))  # Usage message
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
    print("Error: Employee with ID {} not found.".format(employee_id))  # Error message
    sys.exit(1)

# Parse the user information
user_data = user_response.json()
employee_name = user_data['name']  # Employee name

# Make a request to the API to get the todo list information for the employee
todo_url = base_url + 'todos?userId={}'.format(employee_id)
todo_response = requests.get(todo_url)

# Parse the todo list information
todo_data = todo_response.json()
number_of_done_tasks = 0
total_number_of_tasks = len(todo_data)
done_tasks = []

# Find the number of completed tasks and the titles of those tasks
for task in todo_data:
    if task['completed']:
        number_of_done_tasks += 1
        done_tasks.append(task['title'])

# Print the employee's progress report
print("Employee {} is done with tasks({}/{}):".format(employee_name, number_of_done_tasks, total_number_of_tasks))
for task in done_tasks:
    print("\t{}".format(task))

# Export data to CSV file
filename = "{}.csv".format(employee_id)  # CSV file name
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])  # CSV header
    for task in todo_data:
        writer.writerow([employee_id, employee_name, task['completed'], task['title']])  # CSV row

