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

## schema.py

### init_db()
Function for init database with default values

### execute(script, args=None)
Execute passed script with args and return all values with tuple of dicts like this:
```python
from schema import execute
print(execute('select * from workers'))
# ({'worker': u'\u041f\u0430\u0448\u0430', 'id': 1L}, ... )

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