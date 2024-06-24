from flask import request, jsonify, render_template, redirect, url_for, current_app as app
from bson.objectid import ObjectId
from datetime import datetime

@app.route('/')
def home():
    todos = list(app.db['todos'].find().sort([('done', 1), ('_id', 1)]))
    for todo in todos:
        todo['_id'] = str(todo['_id'])
        if 'deadline' in todo:
            todo['deadline'] = todo['deadline'].isoformat()
    return render_template('index.html', todos=todos)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = list(app.db['todos'].find().sort([('done', 1), ('_id', 1)]))
    for todo in todos:
        todo['_id'] = str(todo['_id'])
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = {
        'task': data['task'],
        'done': data.get('done', False),
        'description': data.get('description', ''),
        'deadline': datetime.fromisoformat(data['deadline']) if 'deadline' in data else None
    }
    result = app.db['todos'].insert_one(new_todo)
    new_todo['_id'] = str(result.inserted_id)
    return jsonify(new_todo), 201

@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    update_data = {
        'task': data.get('task'),
        'done': data.get('done'),
        'description': data.get('description'),
        'deadline': datetime.fromisoformat(data['deadline']) if 'deadline' in data else None
    }
    app.db['todos'].update_one({'_id': ObjectId(todo_id)}, {'$set': update_data})
    updated_todo = app.db['todos'].find_one({'_id': ObjectId(todo_id)})
    updated_todo['_id'] = str(updated_todo['_id'])
    return jsonify(updated_todo)

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    app.db['todos'].delete_one({'_id': ObjectId(todo_id)})
    return '', 204

@app.route('/add_todo', methods=['POST'])
def add_todo_form():
    task = request.form.get('task')
    app.db['todos'].insert_one({'task': task, 'done': False, 'description': '', 'deadline': None})
    return redirect(url_for('home'))

@app.route('/edit_todo/<todo_id>', methods=['POST'])
def edit_todo_form(todo_id):
    task = request.form.get('task')
    done = 'done' in request.form
    description = request.form.get('description', '')
    deadline = request.form.get('deadline')
    deadline = datetime.fromisoformat(deadline) if deadline else None
    app.db['todos'].update_one({'_id': ObjectId(todo_id)}, {'$set': {'task': task, 'done': done, 'description': description, 'deadline': deadline}})
    return redirect(url_for('home'))

@app.route('/delete_todo/<todo_id>', methods=['POST'])
def delete_todo_form(todo_id):
    app.db['todos'].delete_one({'_id': ObjectId(todo_id)})
    return redirect(url_for('home'))
