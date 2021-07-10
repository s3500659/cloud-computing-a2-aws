
## How to run the application.

cd into the project folder.
```
cd C:\path\to\the\project\
```

Run the app.
```
python main.py
```


## How to run the unit test files.

Set the PYTHONPATH for the project.

For Windows.
```
set PYTHONPATH=%PYTHONPATH%;C:\path\to\the\project\
```

For UNIX (Linux, OSX, etc...)
```
export PYTHONPATH="${PYTHONPATH}:/path/to/the/project/"
```

Go into the tests folder using the terminal
```
cd tests
```

run the test file. E.g.
```
python test_dynamo_db.py
```

