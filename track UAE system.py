from flask import Flask, request, redirect, session, render_template_string, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'secret123'

USERS = {
    "admin": {"password": "123", "role": "admin"},
    "murhaf": {"password": "123", "role": "user"},
    "khuram": {"password": "123", "role": "user"}
}

TASKS = []

LOGIN_PAGE = '''
<div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column; text-align: center; background-color: #f0f0f0;">
    <h2 style="font-size: 24px;">Field Support Tracker</h2>
    <form method="post" style="width: 300px;">
        <input type="text" name="username" placeholder="Username" required style="width: 100%; margin: 5px; padding: 10px; font-size: 18px;">
        <input type="password" name="password" placeholder="Password" required style="width: 100%; margin: 5px; padding: 10px; font-size: 18px;">
        <button type="submit" style="width: 100%; margin: 5px; padding: 10px; font-size: 18px; background-color: #4CAF50; color: white;">Login</button>
    </form>
</div>
'''


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username]['password'] == password:
            session['user'] = username
            session['role'] = USERS[username]['role']
            return redirect('/dashboard')
        else:
            return "Invalid credentials. Try again."
    return render_template_string(LOGIN_PAGE)


DASHBOARD_PAGE = '''
<div style="text-align: center; background-color: #f0f8ff; padding: 20px;">
    <h2 style="font-size: 28px;">Welcome, {{ session['user'] }}</h2>

    {% if session['role'] == 'admin' %}
    <form method="get" action="/dashboard" style="margin-bottom: 20px;">
        <label style="font-size: 20px;">Select User:</label>
        <select name="user_filter" onchange="this.form.submit()" style="font-size: 18px;">
            <option value="">All Users</option>
            {% for user in USERS.keys() %}
                <option value="{{ user }}" {% if request.args.get('user_filter') == user %}selected{% endif %}>{{ user }}</option>
            {% endfor %}
        </select>
    </form>
    {% endif %}

    <form method="post" style="display:inline-block; text-align: left; width: 400px; background-color: #ffffff; padding: 20px; border-radius: 10px;">
        <h3 style="font-size: 22px;">Add Task</h3>
        <input type="text" name="location" placeholder="Location" required style="width: 100%; margin:5px; padding:10px; font-size: 18px;">
        <input type="text" name="start_time" placeholder="Start Time" required style="width: 100%; margin:5px; padding:10px; font-size: 18px;">
        <input type="text" name="end_time" placeholder="End Time" required style="width: 100%; margin:5px; padding:10px; font-size: 18px;">
        <input type="text" name="description" placeholder="Description" required style="width: 100%; margin:5px; padding:10px; font-size: 18px;">
        <input type="text" name="status" placeholder="Status" required style="width: 100%; margin:5px; padding:10px; font-size: 18px;">
        <input type="text" name="comments" placeholder="Comments" style="width: 100%; margin:5px; padding:10px; font-size: 18px;">
        <button type="submit" style="width: 100%; margin:5px; padding:10px; font-size: 18px; background-color: #2196F3; color: white;">Add Task</button>
    </form>

    <h3 style="font-size: 24px;">Task List</h3>
    <table border="1" style="margin: auto; width: 80%; text-align: left; font-size: 18px; background-color: #ffffff; border-radius: 10px;">
        <tr style="background-color: #d3d3d3;">
            <th>User</th>
            <th>Location</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Description</th>
            <th>Status</th>
            <th>Comments</th>
            <th>Action</th>
        </tr>
        {% for task in tasks %}
            {% if session['role'] == 'admin' and (not request.args.get('user_filter') or task['user'] == request.args.get('user_filter')) %}
                <tr>
                    <td>{{ task['user'] }}</td>
                    <td>{{ task['location'] }}</td>
                    <td>{{ task['start_time'] }}</td>
                    <td>{{ task['end_time'] }}</td>
                    <td>{{ task['description'] }}</td>
                    <td>{{ task['status'] }}</td>
                    <td>{{ task['comments'] }}</td>
                    <td><a href="/delete/{{ task['id'] }}">Delete</a></td>
                </tr>
            {% elif session['role'] == 'user' and task['user'] == session['user'] %}
                <tr>
                    <td>{{ task['user'] }}</td>
                    <td>{{ task['location'] }}</td>
                    <td>{{ task['start_time'] }}</td>
                    <td>{{ task['end_time'] }}</td>
                    <td>{{ task['description'] }}</td>
                    <td>{{ task['status'] }}</td>
                    <td>{{ task['comments'] }}</td>
                    <td><a href="/delete/{{ task['id'] }}">Delete</a></td>
                </tr>
            {% endif %}
        {% endfor %}
    </table>

    <br>
    <a href="/logout" style="font-size: 20px;">Logout</a>
</div>
'''


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        TASKS.append({
            'id': len(TASKS) + 1,
            'user': session['user'],
            'location': request.form['location'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'description': request.form['description'],
            'status': request.form['status'],
            'comments': request.form['comments']
        })

    return render_template_string(DASHBOARD_PAGE, tasks=TASKS, USERS=USERS)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
