#!/usr/bin/python


from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import schema

app = Flask(__name__)

@app.route('/')
def show_tasks():
    tasks = schema.get_tasks_with_workers()
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:id>', methods=['POST', 'GET'])
def task(id):
    if request.method == 'POST':
        schema.change_state(id, request.form.get('state', None))
        return redirect(url_for('show_tasks'))

    workers = schema.get_all_workers()
    task = schema.get_task_with_workers(id)
    return render_template('edit.html', workers=workers, task=task)


if __name__ == '__main__':
	app.run(debug=True)
