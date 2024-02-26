import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from datetime import datetime
from typing import Type

try:
    import robopulser.model_builder as _builder
except ImportError:
    import model_builder as _builder

import logging


modules_to_import = [
    ("mysql.connector", "mysql-connector-python", "mysql_connector"),  # session: OK
    ("pymssql", "pymssql", None),  # session: OK
    ("psycopg2", "psycopg2", None),  # session: OK
    ("pg8000", "pg8000", None),  # session: OK
]

for module_name, pip_name, import_alias in modules_to_import:
    try:
        if import_alias is not None:
            globals()[import_alias] = __import__(pip_name)
        else:
            __import__(pip_name)
    except ImportError:
        pass


class Pulser:

    def __init__(
        self,
        Model: Type[_orm.DeclarativeBase] = None,
        yaml_model_path: str = None,
        conn_str: str = None,
        db_driver: str = None,
        db_user: str = None,
        db_pass: str = None,
        db_host: str = None,
        db_port: str = None,
        db_name: str = None,
        log: logging.Logger = None
    ):

        self.db_driver = db_driver
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.log = log

        self.yaml_model_path = yaml_model_path
        self.conn_str = self._set_conn_str(conn_str)

        print(self.conn_str)

        self.Model = self._set_model(Model, yaml_model_path)

        self.engine = _sql.create_engine(self.conn_str)
        self._create_table()

        self.table = self.Model.__table__
        self.columns = self.table.columns
        self.prime_col = self.table.primary_key.columns[0]
        self.pulse_col = next((c for c in self.columns if c.info == "pulse"), None)

    def _set_model(self, Model, yaml_model_path):
        if yaml_model_path:
            return _builder.build_model_from_yaml(self.yaml_model_path)
        return Model

    def _set_conn_str(self, conn_str):
        if conn_str:
            return self.conn_str

        conn_str_components = (
            self.db_driver,
            self.db_user,
            self.db_pass,
            self.db_host,
            self.db_port,
            self.db_name,
        )

        if all(conn_str_components):
            return f"{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

        return "sqlite:///local_pulse.db"

    def _get_session(self):
        SessionClass = _orm.sessionmaker(bind=self.engine)
        return SessionClass()

    def _create_table(self):
        self.Model.metadata.create_all(bind=self.engine)

    def _db_get_primary_row(self, session):

        filter_dic = {self.prime_col.name: self.prime_col.default.arg}
        try:
            result = session.query(self.Model).filter_by(**filter_dic).one()
        except:
            return None
        return result

    def pulse(self):
        with self._get_session() as session:
            try:
                pulse_column_name = self.pulse_col.name
                pulse_time = datetime.now()

                existing_entry = self._db_get_primary_row(session)
                pulse_time = datetime.now()

                if existing_entry:
                    setattr(existing_entry, pulse_column_name, pulse_time)
                else:
                    query_data = {pulse_column_name: pulse_time}
                    model = self.Model(**query_data)
                    session.add(model)
                session.commit()

                if self.log:
                    self.log.debug(f"Pulsing... [{pulse_time}]")

            except Exception as e:
                if self.log:
                    self.log.error(f"Pulser error: {e}")
                else:
                    print(f"Pulser error: {e}")



if __name__ == "__main__":

    from sqlalchemy import Column, String, Integer, DateTime
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class PulseModel(Base):
        __tablename__ = "PULSE_TABLE"

        id = Column("id", Integer, primary_key=True, autoincrement=True)
        last_pulse = Column("last_pulse", DateTime)
        alert_contact = Column("alert_contact", String(1000))



    pulser = Pulser(yaml_model_path="pulse_table.yml")
    row = pulser.pulse()