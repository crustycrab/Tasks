Tasks
=====

##All u need is:
	
1. MySQL server
2. Flask
3. Python
4. MySQL python client

Needed packages: python, python-mysqldb, mysql-client, python-flask

##Launch

1. Change db configuration in in scheme.py
2. Init database with init_db.py if needed
3. Run run run.py
4. 127.0.0.1:5000

## Tables

### tasks
id | date | task | result
--- | --- | --- | ---
1 | 2014-05-15 12:00:03 | Really hard task | 0

### workers
id | worker
--- | ---
1 | John

### task_logs
id | task_id | log
--- | --- | ---
1 | 1 | Log message

### classes
id | task_id | worker_id
1 | 1 | 1

## schema.py

### init_db()
Function for init database with default values

### execute(script, args=None)
Execute passed script with args and return all values with tuple of dicts like this:
```python
from schema import execute
print(execute('select * from workers'))
# ({'worker': u'\u041f\u0430\u0448\u0430', 'id': 1L}, ...)

script = 'insert into tasks (task, result) values (%s, %s)'
print(execute(scipt, ('Something useful', '1')))
# ()
```

### log(id, message)
Simple log passed message for tasks id
```python
from schema import log
log(1, 'Test message')
```

### Some other funtions
```python
from schema import check_id
print(check_id(1)) # Check id in tasks table or not
# True

print(get_all_workers()) # Tuple with all workers
# ({'worker': u'\u041f\u0430\u0448\u0430', 'id': 1L}, ...)

print(get_workers_by_id(1)) # Tuple with workers in task with passed id
# ({'worker': u'\u0412\u0430\u0434\u0438\u043c', 'id': 2L}, ...)

print(get_tasks()) # Tuple with all tasks
# ({'date': datetime.datetime(2014, 5, 19, 22, 57), 'task': u'Something useful', 'id': 6L, 'result': 1}, ...)

print(get_task(1)) # Task by id
# {'date': datetime.datetime(2014, 5, 14, 17, 16, 34), 'task': u'\u0423\u0431\u0440\u0430\u0442\u044c\u0441\u044f \u0432 \u0434\u043e\u043c\u0435', 'id': 1L, 'result': 0}

print(get_tasks_with_workers()) # All tasks with current workers
# ({'date': datetime.datetime(2014, 5, 19, 22, 57), 'workers': (), 'task': u'Something useful', 'id': 6L, 'result': 1}, ...)

print(get_task_with_workers(1)) # Single task with current workers
# {'date': datetime.datetime(2014, 5, 14, 17, 16, 34), 'workers': ({'worker': u'\u0412\u0430\u0434\u0438\u043c', 'id': 2L}, {'worker': u'\u0413\u0435\u043d\u043d\u0430\u0434\u0438\u0439', 'id': 4L}), 'task': u'\u0423\u0431\u0440\u0430\u0442\u044c\u0441\u044f \u0432 \u0434\u043e\u043c\u0435', 'id': 1L, 'result': 0}

print(get_logs(1))
# {'date': datetime.datetime(2014, 5, 14, 17, 16, 34), 'Log message'}

# Change values functions
change_state(1, 0) # Change state of task by id

change_task_text(1, 'New text') # Change text of task by id

change_workers(1, {'Worker1': 1, 'Worker2': 4}) # Change current workers in task by id, dict(worker_name: id), 
```