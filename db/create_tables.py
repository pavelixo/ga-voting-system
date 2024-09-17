from sqlalchemy import inspect
from db.database import engine, Base

def create_tables_if_not_exists():
  inspector = inspect(engine)
  if 'candidates' not in inspector.get_table_names():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
  else:
    print("Tables already exist. Skipping creation.")
