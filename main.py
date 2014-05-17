#!/usr/bin/python
#-*-encoding: utf-8-*-

from flask import Flask, request, redirect, url_for, render_template

import schema

app = Flask(__name__)

@app.route('/')
def show_tasks():
    tasks = schema.get_tasks_with_workers()
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:id>', methods=['POST', 'GET'])
def task(id):
    if request.method == 'POST':
        schema.change_state(id, request.form.get('state'))
        schema.change_workers(id, request.form)
        schema.change_task_text(id, request.form.get('task_text'))
        return redirect(url_for('show_tasks'))

    task = schema.get_task_with_workers(id)
    all_workers = schema.get_all_workers()
    logs = schema.get_logs(id)
    return render_template('edit.html', all_workers=all_workers, task=task, logs=logs)


if __name__ == '__main__':
	app.run(debug=True)
