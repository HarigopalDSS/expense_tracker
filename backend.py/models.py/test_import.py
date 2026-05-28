import sys
import traceback
sys.path.insert(0, '.')
try:
    from fastapi import FastAPI
    print("FastAPI OK")
    from database import SessionLocal, engine, Base
    print("Database OK")
    import models
    print("Models OK")
    from schemas import ExpenseCreate
    print("Schemas OK")
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables OK")
    app = FastAPI()
    print(f"App created: {app}")
    print("SUCCESS!")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
