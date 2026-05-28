from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect(
    "expenses.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    category TEXT,
    expense_date TEXT
)
""")

conn.commit()


class Expense(BaseModel):
    n: str
    a: float
    c: str
    d: str


@app.post("/add_exp")
def add_exp(exp: Expense):
    cursor.execute(
        """
        INSERT INTO expenses
        (name,amount,category,expense_date)
        VALUES(?,?,?,?)
        """,
        (
            exp.n,
            exp.a,
            exp.c,
            exp.d
        )
    )
    conn.commit()
    return {"message": "Expense Added Successfully"}


@app.get("/view_exp")
def view_exp():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    data = []
    for i in rows:
        data.append({
            "id": i[0],
            "name": i[1],
            "amount": i[2],
            "category": i[3],
            "expense_date": i[4]
        })

    return data


@app.put("/upd_exp/{id}")
def update_exp(id: int, exp: Expense):
    cursor.execute(
        """
        UPDATE expenses
        SET
        name=?,
        amount=?,
        category=?,
        expense_date=?
        WHERE id=?
        """,
        (
            exp.n,
            exp.a,
            exp.c,
            exp.d,
            id
        )
    )

    conn.commit()

    if cursor.rowcount > 0:
        return {"message": "Updated Successfully"}

    return {"message": "Expense Not Found"}


@app.delete("/delete_exp/{id}")
def delete_exp(id: int):
    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        return {"message": "Deleted Successfully"}

    return {"message": "Expense Not Found"}


@app.get("/srh_exp/{id}")
def search_exp(id: int):
    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE id=?
        """,
        (id,)
    )

    row = cursor.fetchone()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "amount": row[2],
            "category": row[3],
            "expense_date": row[4]
        }

    return {"message": "Expense Not Found"}


@app.get("/sort_exp/{sort_by}/{order}")
def sort_exp(sort_by: str, order: str):
    allowed_cols = ["id", "name", "amount", "category", "expense_date"]

    if sort_by not in allowed_cols:
        return {"message": "Invalid Column"}

    if order not in ["ASC", "DESC"]:
        return {"message": "Invalid Order"}

    query = f"""
    SELECT *
    FROM expenses
    ORDER BY {sort_by} {order}
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for i in rows:
        data.append({
            "id": i[0],
            "name": i[1],
            "amount": i[2],
            "category": i[3],
            "expense_date": i[4]
        })

    return data
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect(
    "expenses.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    category TEXT,
    expense_date TEXT
)
""")

conn.commit()

class Expense(BaseModel):
    n: str
    a: float
    c: str
    d: str

@app.post("/add_exp")
def add_exp(exp: Expense):

    cursor.execute(
        """
        INSERT INTO expenses
        (name,amount,category,expense_date)
        VALUES(?,?,?,?)
        """,
        (
            exp.n,
            exp.a,
            exp.c,
            exp.d
        )
    )

    conn.commit()

    return {
        "message": "Expense Added Successfully"
    }

@app.get("/view_exp")
def view_exp():

    cursor.execute(
        "SELECT * FROM expenses"
    )

    rows = cursor.fetchall()

    data = []

    for i in rows:
        data.append({
            "id": i[0],
            "name": i[1],
            "amount": i[2],
            "category": i[3],
            "expense_date": i[4]
        })

    return data

@app.put("/upd_exp/{id}")
def update_exp(id: int, exp: Expense):

    cursor.execute(
        """
        UPDATE expenses
        SET
        name=?,
        amount=?,
        category=?,
        expense_date=?
        WHERE id=?
        """,
        (
            exp.n,
            exp.a,
            exp.c,
            exp.d,
            id
        )
    )

    conn.commit()

    if cursor.rowcount > 0:

        return {
            "message": "Updated Successfully"
        }

    return {
        "message": "Expense Not Found"
    }

@app.delete("/delete_exp/{id}")
def delete_exp(id: int):

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()

    if cursor.rowcount > 0:

        return {
            "message": "Deleted Successfully"
        }

    return {
        "message": "Expense Not Found"
    }

@app.get("/srh_exp/{id}")
def search_exp(id: int):

    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE id=?
        """,
        (id,)
    )

    row = cursor.fetchone()

    if row:

        return {
            "id": row[0],
            "name": row[1],
            "amount": row[2],
            "category": row[3],
            "expense_date": row[4]
        }

    return {
        "message": "Expense Not Found"
    }

@app.get("/sort_exp/{sort_by}/{order}")
def sort_exp(
    sort_by: str,
    order: str
):

    allowed_cols = [
        "id",
        "name",
        "amount",
        "category",
        "expense_date"
    ]

    if sort_by not in allowed_cols:

        return {
            "message": "Invalid Column"
        }

    if order not in [
        "ASC",
        "DESC"
    ]:

        return {
            "message": "Invalid Order"
        }

    query = f"""
    SELECT *
    FROM expenses
    ORDER BY {sort_by} {order}
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    data = []

    for i in rows:

        data.append({
            "id": i[0],
            "name": i[1],
            "amount": i[2],
            "category": i[3],
            "expense_date": i[4]
        })

    return data