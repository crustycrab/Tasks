#!/usr/bin/python

import MySQLdb as mdb
import os
import re
from time import gmtime, strftime


def connect_db():
    host = 'localhost'
    user = 'crusty'
    password = 'x'
    db_name = 'testdb'
    return mdb.connect(
        host, user, password, db_name)


def exec_sql_file(cursor, sql_file):
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):
            continue
        if not re.search(r'[^-;]+;', line):
            statement = statement + line
        else:
            statement = statement + line
            try:
                cursor.execute(statement)
            except Exception as e:
                print(str(e.args))

            statement = ""


def execute(cursor, script):
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    log_message = 'LOG[%s]' % time
    errors = None
    try:
        cursor.execute(script)
    except Exception, e:
        errors = str(e.args)
    finally:
        log_message += ' executed:\n\t"%s"\n' % script
        if errors:
            log_message += '\tERORS: %s\n'

        log(log_message)


def log(message):
    with open("log.txt", "a") as logfile:
        logfile.write(message)


def init_db():
    connection = connect_db()
    with connection:
        cursor = connection.cursor()
        exec_sql_file(cursor, os.path.abspath('schema.sql'))
        with open('log.txt', 'w') as logfile:
            logfile.write('DATABASE INITED\n')


def decode_row(row, encoding='utf-8'):
    def _decode(value):
        if type(value) is str:
            return value.decode(encoding)
        return value

    if type(row) is dict:
        return {key: _decode(value) for key, value in row.iteritems()}
    if type(row) in (tuple, list):
        return [_decode(value) for value in row]
    return row


def get_workers_by_id(id):
    connection = connect_db()
    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)
        script = 'select workers.id, workers.worker \
			from workers join classes \
			on classes.worker_id = workers.id and classes.task_id = %d \
			order by classes.task_id;' % id
        execute(cursor, script)
    return [decode_row(worker) for worker in cursor.fetchall()]


def get_all_workers():
    connection = connect_db()
    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)
        script = 'select * from workers;'
        execute(cursor, script)
    return [decode_row(worker) for worker in cursor.fetchall()]


def get_tasks():
    connection = connect_db()
    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute('select * from tasks order by date desc;')
    return [decode_row(row) for row in cursor.fetchall()]


def get_tasks_with_workers():
    tasks = get_tasks()
    for i, task in enumerate(tasks):
        tasks[i]['workers'] = get_workers_by_id(task['id'])
    return tasks


def get_task(id):
    connection = connect_db()
    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)
        script = 'select * from tasks where id = %d;' % id
        execute(cursor, script)
    return decode_row(cursor.fetchone())


def get_task_with_workers(id):
    task = get_task(id)
    task['workers'] = get_workers_by_id(id)
    return task


def change_state(id, result):
    connection = connect_db()
    with connection:
        cursor = connection.cursor()
        if not result is None:
            script = 'update tasks set result=%d where id=%d;' % (int(result), int(id))
            execute(cursor, script)

def change_workers(id, form):
	actual_workers = get_workers_by_id(id)
	all_workers = get_all_workers()
	connection = connect_db()
	with connection:
		cursor = connection.cursor()
		for worker in actual_workers:
			if not worker['worker'] in form:
				script = 'delete from classes where task_id=%d and worker_id=%d;' % (int(id), int(worker['id']))
				execute(cursor, script)
		for worker in all_workers:
			worker_id = form.get(worker['worker'])
			if not worker_id is None and worker not in actual_workers:
				script = 'insert into classes (task_id, worker_id) values (%d, %d);' % (int(id), int(worker_id))
				execute(cursor, script)

if __name__ == '__main__':
    init_db()
