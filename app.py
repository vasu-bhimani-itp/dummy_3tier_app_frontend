from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)



BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

@app.route('/')
def index():
    try:
        response = requests.get(f"{BACKEND_URL}/tasks", timeout=3)

        if response.status_code == 200:
            tasks = response.json()
        else:
            print("Backend returned error:", response.status_code)
            tasks = []

    except requests.exceptions.RequestException as e:
        print("Backend not reachable:", e)
        tasks = []

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    requests.post(f"{BACKEND_URL}/tasks", json={"title": title})
    return redirect('/')

@app.route('/update/<id>', methods=['POST'])
def update(id):
    requests.put(f"{BACKEND_URL}/tasks/{id}", json={"status": "completed"})
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    requests.delete(f"{BACKEND_URL}/tasks/{id}")
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)