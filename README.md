# robopulse

NOTE: This project is in ealry stage!

This is robopulser—a small, single-task library. It is meant to update a timestamp in a database. The robopulser library is built around the SQLAlchemy package and is relatively open for customization.

## Why you would need such a thing?

If your program performs actions like RPA automation and you'd like to have constant updates from the program to a database, robopulse is for you. Although it is written in Python and can be imported directly into Python code, it can also work as a stand-alone script with a single YAML configuration file.

## Installation

For testing without any database:

```powershell
pip install robopulser
```

If you want to use robopulse with a real database (not SQLite), you can download it with one of the optional dependencies. The following databases have been tested and proven working:

```powershell
pip install robopulser[mssql]         # pip install pymssql
pip install robopulser[mysql]         # pip install mysql-connector-python
pip install robopulser[postgress]     # pip install psycopg2
pip install robopulser[postgress1]    # pip install pg8000
```

## Using in Python script

There are two ways to use robopulser inside the Python script. You can use it with your own SQLAlchemy model, or let robopulser create an SQLAlchemy model for you using a simple YAML file containing database table parameters and a few important flags.

### Using with YAML file

Note that the configuration file is always the same among various databases. You can test robopulser using a local SQLite database (which is generated automatically by robopulser). And when you are ready to go live, just replace the connection parameters.

Look at the example of the configuration file (`example.yml`):

```yaml
table_name: "PULSE_TABLE"

columns:

    # Mandatory: `primary_key=True` (but column name can be any)
  - name: pid
    column_type: String(1000)
    default: "UNIQUEPID-123"
    unique: True
    primary_key: True          # <--- IMPORTANT

    # Mandatory: `info: 'pulse'` and type DateTime (but column name can be any)
  - name: last_pulse
    column_type: DateTime
    info: 'pulse'              # <--- IMPORTANT

    # No special tags, just a regular (optional) column example 
  - name: contact_info         
    column_type: String(1000)
    default: "emergency.contact@mail.com"
    
    # You can add more columns with data you want to monitor
    # - name: (...) 
```

Now save this configuration as `example.yml` and (in the same directory) write a simple script:

```python
import robopulser.robopulser as pulser

pulser.yaml_pulse("example.yml")
```

Without providing any additional parameters, robopulser will create a local SQLite database (`local_pulse.db`) and send a pulse to it.

You will not see any logs, but you can add a logger (from Python's logging library), and robopulse will send a single log at the debug level. A recommended logger is [robolog](https://pypi.org/project/robolog/), which is already optimized for RPA purposes.

### Using with SQLAlchemy Models

If you want to use robopulse inside your code using your own SQLAlchemy model class, you can do it as well. Let's reproduce the previous example in this way:

```python
# roboforge-solutions's suite:
import robopulser.robopulser as pulser
from robolog import robolog

# sqlalchemy imports:
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base


# Creating robolog instance:
log = robolog.get_logger()

# Your own model class:
Base = declarative_base()
class MyPulseModel(Base):
    __tablename__ = "PULSE_TABLE"

    pid = Column("pid", String(100), primary_key=True, unique=True, default="UNIQUEPID-123")
    last_pulse = Column("last_pulse", DateTime, info="pulse")
    contact_info = Column("contact_info", String(1000), default="emergency.contact@mail.com")

# Single pulse using model approach:
pulser.model_pulse(Model=MyPulseModel, logger=log)
```

## Using outside Python script

In order to be able to run this as a stand-alone program that can be compiled to an `.exe` file or just launched from the console, you can modify the previous example by giving an argument parser. Also, you can use a shell script provided by the robolog library to get ready-to-use examples. After installing the robolog library, just type in your shell (tested on PowerShell, Windows 11):

```powershell
(venv) PS C:\Users\jankiwoj_box\Documents\projects\_test> pulser-template
Got template: example.yml
Got template: pulser.py
```

You will get a YAML file (the same as in the first example) and the run script recognizing this YAML.

You can give some flags to this script. Learn more using the -h flag:

```powershell
(venv) PS C:\Users\jankiwoj_box\Documents\projects\_test> python .\pulser.py -h
usage: pulser.py [-h] [--yaml YAML] [--conn_str CONN_STR] [--driver DRIVER] [--user USER] [--host HOST] [--name NAME] [--passwd PASSWD] [--port PORT]

Script to call robopulser.yaml_pulse function with optional arguments.

options:
  -h, --help           show this help message and exit
  --yaml YAML          Path to YAML model configuration file
  --conn_str CONN_STR  Connection string (alternative to remaining parameters.)
  --driver DRIVER      Database driver
  --user USER          Database user
  --host HOST          Database host
  --name NAME          Database name
  --passwd PASSWD      Database password
  --port PORT          Database port
```

Note: you cannot pass a logger using parameters, but you can edit `pulser.py` script and pass your logger straight into the `yaml_pulse` function in the same way as in the previous example.
