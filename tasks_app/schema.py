#-*-encoding: utf-8-*-

import MySQLdb as mdb
import os
import re
from time import gmtime, strftime

from tasks_app import app

DB_CHARSET = 'utf8'
DB_HOST = 'localhost'
DB_USER = 'crusty'
DB_PASSWORD = 'x'
DB_NAME = 'testdb'
DB_USE_UNICODE = True

STATES = (u'Решено', u'В процессе', u'Отменено')


def connect_db():
    """Returning connection object"""
    return mdb.connect(
        DB_HOST, DB_USER, DB_PASSWORD,
        DB_NAME, charset=DB_CHARSET,
        use_unicode=DB_USE_UNICODE)


def get_time():
    """Just current time"""
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


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
                pass

            statement = ""


def execute(script, args=None):
    """execute(script) executed passed script"""
    connection = connect_db()
    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute(script, args)
    return cursor.fetchall()


def log(id, message):
    """log(id, message) logging passed message
    to task id to table task_logs"""
    time = get_time()
    script = re.sub(r'\s+', ' ', message)
    connection = connect_db()
    with connection:
        cursor = connection.cursor()
        script = 'insert into task_logs (date, task_id, log) values (now(), %s, %s)'
        execute(script, (id, message))


def init_db():
    """Init database"""
    connection = connect_db()
    with connection:
        cursor = connection.cursor()
        exec_sql_file(cursor,
                      os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql'))


def get_workers_by_id(id):
    script = 'select workers.id, workers.worker \
		from workers join classes \
		on classes.worker_id = workers.id and classes.task_id = %s \
		order by classes.task_id;'
    return execute(script, (id, ))


def get_all_workers():
    script = 'select * from workers;'
    return execute(script)


def get_tasks():
    script = 'select * from tasks order by date desc;'
    return execute(script)


def get_tasks_with_workers():
    tasks = get_tasks()
    for i, task in enumerate(tasks):
        tasks[i]['workers'] = get_workers_by_id(task['id'])
    return tasks


def get_task(id):
    script = 'select * from tasks where id=%s;'
    return execute(script, (id,))[0]


def get_task_with_workers(id):
    task = get_task(id)
    task['workers'] = get_workers_by_id(id)
    return task


def change_state(id, result):
    current_result = get_task(id)['result']
    if not result is None and int(result) != current_result:
        script = 'update tasks set result=%s where id=%s;'
        execute(script, (result, id))
        message = u'Новое состояние задания: "%s"' % STATES[int(result)]
        log(id, message)


def change_task_text(id, text):
    current_text = get_task(id)['task']
    if text != '' and text != current_text:
        script = 'update tasks set task=%s where id=%s'
        execute(script, (text, id))
        message = u'Текст изменен: "%s"' % text
        log(id, message)


def change_workers(id, form):
    actual_workers = get_workers_by_id(id)
    all_workers = get_all_workers()

    for_log = []
    values = []
    for worker in actual_workers:
        script = 'delete from classes where task_id=%s and worker_id=%s;'
        if not worker['worker'] in form:
            execute(script, (id, worker['id']))
            for_log.append(worker['worker'])
    if len(for_log) > 0:
        message = u'Удалены исполнители: "%s"' % ', '.join(for_log)
        log(id, message)

    for_log = []
    for worker in all_workers:
        worker_id = form.get(worker['worker'])
        script = 'insert into classes (task_id, worker_id) values (%s, %s);'
        if not worker_id is None and worker not in actual_workers:
            execute(script, (id, worker_id))
            for_log.append(worker['worker'])
    if len(for_log) > 0:
        message = u'Добавлены исполнители: "%s"' % ', '.join(for_log)
        log(id, message)


def get_logs(id):
    script = 'select date, log from task_logs where task_id = %s'
    return execute(script, (id,))
