from fastapi import APIRouter,HTTPException
from .storage import get_all_tasks,add_task,get_task_by_id,update_task,delete_task
from .models import TaskCreate,TaskUpdate,TaskResponse
router=APIRouter(prefix="/api/tasks",tags=["tasks"])
from typing import Optional

@router.get("",response_model=list[TaskResponse])
def gt(status: Optional[str] = None, priority: Optional[str] = None): return get_all_tasks(status=status, priority=priority)
@router.post("",response_model=TaskResponse,status_code=201)
def ct(p:TaskCreate): return add_task(p)
@router.get("/{task_id}",response_model=TaskResponse)
def g(task_id:str):
 t=get_task_by_id(task_id)

 if not t:
     raise HTTPException(404,"Not found"); 
 return t
@router.put("/{task_id}",response_model=TaskResponse)
def u(task_id:str,p:TaskUpdate):
 t=update_task(task_id,p)

 if not t:
     raise HTTPException(404,"Not found"); 
 return t
@router.delete("/{task_id}",status_code=204)
def d(task_id:str):
 if not delete_task(task_id): 
     raise HTTPException(404,"Not found")
