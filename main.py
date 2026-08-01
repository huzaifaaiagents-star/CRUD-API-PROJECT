from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

from pydantic import BaseModel

class NewTask(BaseModel):
    title: str = ""

tasks_list = [
    { "title": "Task_1", "id": 0, "done": True},
    { "title": "Task_2", "id": 1, "done": False},
    { "title": "Task_3", "id": 2, "done": False},
]

@app.get("/")
def api_info():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks_list

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks_list:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.post("/tasks", status_code=201)
def create_task(task: NewTask):
    if not task.title:
        return JSONResponse(status_code=400, content={"error": "title is required"})
    new_task = {"title": task.title, "id": len(tasks_list), "done": False}
    tasks_list.append(new_task)
    return new_task

from typing import Optional

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{id}")
def update_task(id: int, updated_task: TaskUpdate):
    if updated_task.title is None and updated_task.done is None:
        return JSONResponse(status_code=400, content={"error": "no fields to update"})
    for task in tasks_list:
        if task["id"] == id:
            if updated_task.title is not None:
                task["title"] = updated_task.title
            if updated_task.done is not None:
                task["done"] = updated_task.done
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for task in tasks_list:
        if task["id"] == id:
            tasks_list.remove(task)
            return
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

