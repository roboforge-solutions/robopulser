try:
    from robopulser.pulser import Pulser
except ImportError:
    from pulser import Pulser


# For type hinting
import sqlalchemy.orm as _orm
from typing import Type
import logging


def yaml_pulse(
    yaml_model_path: str,
    conn_str: str = None,
    db_driver: str = None,
    db_user: str = None,
    db_pass: str = None,
    db_host: str = None,
    db_port: str = None,
    db_name: str = None,
    logger: logging.Logger = None,
):
    """
    Create or update a database record using the specified YAML model configuration.

    Parameters:
    - yaml_model_path (str): Path to the YAML file containing the model configuration.
    - conn_str (str, optional): Database connection string. If not provided, a default local SQLite connection is used.
    - db_driver (str, optional): Database driver (currently one of: 'mssql+pymssql', 'mysql+mysqlconnector', 'postgresql+psycopg2', 'postgresql+pg8000').
    - db_user (str, optional): Database username. Leave empty if conn_str provided.
    - db_pass (str, optional): Database password. Leave empty if conn_str provided.
    - db_host (str, optional): Database host address. Leave empty if conn_str provided.
    - db_port (str, optional): Database port. Leave empty if conn_str provided.
    - db_name (str, optional): Name of the database. Leave empty if conn_str provided.
    - logger (logging.Logger, optional): Logger object for logging messages. Your logger (robolog preferred).

    Returns:
    None
    """
    pulser = Pulser(
        yaml_model_path=yaml_model_path,
        conn_str=conn_str,
        db_driver=db_driver,
        db_user=db_user,
        db_pass=db_pass,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        log=logger,
    )
    pulser.pulse()


def model_pulse(
    Model: Type[_orm.DeclarativeBase],
    conn_str: str = None,
    db_driver: str = None,
    db_user: str = None,
    db_pass: str = None,
    db_host: str = None,
    db_port: str = None,
    db_name: str = None,
    logger: logging.Logger = None,
):
    """
    Create or update a database record using the specified SQLAlchemy model class.

    Parameters:
    - Model (Type[_orm.DeclarativeBase]): SQLAlchemy DeclarativeBase model class.
    - conn_str (str, optional): Database connection string. If not provided, a default local SQLite connection is used.
    - db_driver (str, optional): Database driver (currently one of: 'mssql+pymssql', 'mysql+mysqlconnector', 'postgresql+psycopg2', 'postgresql+pg8000').
    - db_user (str, optional): Database username. Leave empty if conn_str provided.
    - db_pass (str, optional): Database password. Leave empty if conn_str provided.
    - db_host (str, optional): Database host address. Leave empty if conn_str provided.
    - db_port (str, optional): Database port. Leave empty if conn_str provided.
    - db_name (str, optional): Name of the database. Leave empty if conn_str provided.
    - logger (logging.Logger, optional): Logger object for logging messages. Your logger (robolog preferred).

    Returns:
    None
    """
    pulser = Pulser(
        Model=Model,
        conn_str=conn_str,
        db_driver=db_driver,
        db_user=db_user,
        db_pass=db_pass,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        log=logger,
    )
    pulser.pulse()


if __name__ == "__main__":

    from sqlalchemy import Column, String, Integer, DateTime
    from sqlalchemy.orm import declarative_base
    import time

    # Test pulsing from yaml-generated table
    # yaml_pulse("pulse_table.yml")
    # time.sleep(1)

    # # Test pulsing from own Model class:
    # Base = declarative_base()

    # class PulseTable(Base):
    #     __tablename__ = "PULSE_TABLE"

    #     pid = Column(
    #         "pid", String(1000), unique=True, primary_key=True, default="UNIQUEID-420"
    #     )
    #     last_pulse = Column("last_pulse", DateTime, info="pulse")
    #     contact_info = Column("contact_info", String, default="my@mail.com")

    # model_pulse(Model=PulseTable)

    # ---------------------------------------------------------------------------------------------------------------------
    # DOCKER DB TESTING SETUP:

    # Folllowing instructions are in first place for me to be able to repoduce testing setup but feel free to play with it.
    # Just for informative purposes, should help to reproduce my results (used manually while installing docker images):
    # How to test (on Windows computer with admin rights):
    # 1. Install docker desktop
    # 2. Add docker command binary to $PATH and restart poweshell
    # 3. Visit url: test_sources[<selected database type>] and confirm following commands (manually or write your own script):
    # 4. Execute in PowerShell: command which is assigned to `pull` keyword
    # 5. Execute in PowerShell: command which is assigned to `run` keyword
    # 6. Confirm in your Docker desktop that given container is running
    # 7. Make sure, you have all necessary python libs installed in your venv.
    # 8. RUN THIS SCRIPT FROM YOUR DRIVE, dockers and db's inside them should be available from outside.

    test_sources = {
        "mssql": {
            "url": "https://hub.docker.com/_/microsoft-mssql-server/",
            "pull": "docker pull mcr.microsoft.com/mssql/server",
            "run": 'docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=yourStrong(!)Password" -e "MSSQL_PID=Evaluation" -p 1433:1433  --name sqlpreview --hostname sqlpreview -d mcr.microsoft.com/mssql/server',
        },
        "mysql": {
            "url": "https://hub.docker.com/_/mysql/",
            "pull": "docker pull mysql",
            "run": "docker run -e MYSQL_ROOT_PASSWORD=yourStrongPassword -p 3306:3306 --name mysql_container -d mysql",
        },
        "postgress": {
            "url": "https://hub.docker.com/_/postgres/",
            "pull": "docker pull postgres",
            "run": "docker run -e POSTGRES_PASSWORD=yourStrongPassword -p 5432:5432 --name postgres_container -d postgres",
        },
    }

    # Data used for testing. This data is provided manually based on the settings of docker images above.
    test_setup = {
        "mssql-pymssql": {
            "user": "sa",
            "password": "yourStrong(!)Password",
            "host": "localhost",
            "port": "1433",
            "db_name": "master",
            "driver": "mssql+pymssql",
        },
        "mysql": {
            "user": "root",
            "password": "yourStrongPassword",
            "host": "localhost",
            "port": "3306",
            "db_name": "mysql",
            "driver": "mysql+mysqlconnector",
        },
        "postgress-psycopg2": {
            "user": "postgres",
            "password": "yourStrongPassword",
            "host": "localhost",
            "port": "5432",
            "db_name": "postgres",
            "driver": "postgresql+psycopg2",
        },
        "postgress-pg8000": {
            "user": "postgres",
            "password": "yourStrongPassword",
            "host": "localhost",
            "port": "5432",
            "db_name": "postgres",
            "driver": "postgresql+pg8000",
        },
    }

    for driver, params in test_setup.items():
        user = params["user"]
        passwd = params["password"]
        host = params["host"]
        port = params["port"]
        name = params["db_name"]
        driver = params["driver"]

        yaml_pulse("pulse_table.yml", None, driver, user, passwd, host, port)
