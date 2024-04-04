import os
import subprocess
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/start")
def start(start_with: int = 0):

    if not hasattr(app, "sub"):
        app.sub = subprocess.Popen(
            f"../venv/Scripts/python ../robot/robot.py --start_with={start_with}"
        )
        return {"result": "robot - start"}
    else:
        return {"result": "robot - is running"}


@app.get("/stop")
def stop():
    if hasattr(app, "sub"):
        app.sub.terminate()
        subprocess.Popen("../venv/Scripts/python ../robot/database.py")
        return {"result": "robot - stop"}
    else:
        return {"result": "robot - not start"}


@app.get("/robots", response_model=list[schemas.Robot])
def show(db: Session = Depends(get_db)):
    robots = crud.get_robots(db)
    return robots


@app.get("/", response_class=HTMLResponse)
async def show_robots(request: Request, db: Session = Depends(get_db)):

    robots = crud.get_robots(db)

    return templates.TemplateResponse(
        request=request, name="item.html", context={"robots": robots}
    )
