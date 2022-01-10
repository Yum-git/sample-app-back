import sqlite3

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from model.plan import CreatePlan, UpdatePlan, DeletePlan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000',
                   'http://localhost:5000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

DB_NAME = "sample.db"
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


@app.get("/")
async def root():
    return {"Hello": "World!!"}


@app.post("/plan")
async def create_plan(plan: CreatePlan) -> None:
    cur.execute("INSERT INTO plan(start_date, end_date, title, notes) "
                "VALUES(?, ?, ?, ?)",
                (plan.start_date,
                 plan.end_date,
                 plan.title,
                 plan.notes))
    conn.commit()

    return


@app.get("/plan")
async def read_plan() -> dict:
    cur.execute("SELECT id, start_date as startDate, end_date as endDate, "
                "title, notes "
                "FROM plan ")

    response = cur.fetchall()
    return {"results": response}


@app.put("/plan")
async def update_plan(plan: UpdatePlan) -> None:
    cur.execute(
        "UPDATE plan SET "
        "start_date = CASE WHEN ? IS NOT NULL THEN ? ELSE start_date END, " 
        "end_date = CASE WHEN ? IS NOT NULL THEN ? ELSE end_date END, "
        "title = CASE WHEN ? IS NOT NULL THEN ? ELSE title END, "
        "notes = CASE WHEN ? IS NOT NULL THEN ? ELSE notes END "
        "WHERE id = ? ",
        (plan.start_date, plan.start_date,
         plan.end_date, plan.end_date,
         plan.title, plan.title,
         plan.notes, plan.notes,
         plan.id))

    conn.commit()

    return


@app.delete("/plan")
async def delete_plan(plan: DeletePlan) -> None:
    cur.execute("DELETE FROM plan WHERE id = ?",
                (plan.id,))
    conn.commit()

    return
