from fastapi import FastAPI,Depends
from database import Base, engine,ToDo,SessionLocal
from pydantic import BaseModel
from sqlalchemy.orm import Session

class ToDoRequest(BaseModel):
    task: str


Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
        

app = FastAPI()

@app.post("/todo")
def create_todo(todo: ToDoRequest):
    session = Session(bind=engine, expire_on_commit=False)  # create a new database
    tododb = ToDo(task = todo.task) # create an instance of the ToDo database model
    session.add(tododb)
    session.commit()
    # id = tododb.id
    task=tododb.task
    #  session.close()
    # return the id
    return f"created todo item with todo task {todo.task}"

@app.post("/create_todo_list/")
def details_input(request:ToDoRequest,db: Session = Depends(get_db)):
    new_task = ToDo(task=request.task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message":"list created successfully"}

@app.get("/todo_list/")
def read_todo(db:Session = Depends(get_db)):
    task = db.query(ToDo).all()
    print(task)
    return {"read todo item ":task}


@app.get("/todo/{id}")
def read_todo(id,db:Session = Depends(get_db)):
    task = db.query(ToDo).filter(ToDo.id==id).first()
    if task:
        return {"read todo item ":task}


@app.delete("/todo/{id}")
def delete_todo(id,db:Session=Depends(get_db)):
    delete_task=db.query(ToDo).filter(ToDo.id==id).delete()
    db.commit()
    return f"delete todo item with id {id}"

@app.put("/update_todo/{id}")
def updated_todo(id,request:ToDoRequest,db:Session=Depends(get_db)):
    updated_task=db.query(ToDo).filter(ToDo.id==id)
    print(updated_task)
    if updated_task:
     updated_task.update(request.model_dump())
     db.commit()
     return f"updated list {id}"
