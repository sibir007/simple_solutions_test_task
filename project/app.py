from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
async def run_task(payload = Body(...)):
    task_type = payload["type"]
    return JSONResponse(task_type)


@app.get("/tasks/{task_id}")
async def get_status(task_id):
    return JSONResponse(task_id)
