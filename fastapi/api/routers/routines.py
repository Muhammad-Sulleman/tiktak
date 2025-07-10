from fastapi import APIRouter , HTTPException,status
from api.models import Routine ,Workout
from typing import Optional,List
from pydantic import BaseModel
from api.deps import db_dependency ,user_dependency
from sqlalchemy.orm import joinedload

router=APIRouter(
    prefix="/routines",
    tags=["routines"]
)
class Routines(BaseModel):
    name:str
    description:Optional [str]=None
class CreateRoutine(Routines):
    workouts:List[int]=[]
@router.get('/')
def get_routines(db:db_dependency,user:user_dependency):
    routines=db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id==user.get('id')).all()
    if not routines:
        raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Routines not found"
)
    return routines

@router.post('/')
def create_routine(db:db_dependency,user:user_dependency,routine:CreateRoutine):
    db_routine=Routine(name=routine.name,description=routine.description,user_id=user.get('id'))
    for workout_id in routine.workouts:
        workout=db.query(Workout).filter(Workout.id==workout_id).first()
        if workout:
            db_routine.workouts.append(workout)
         
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    db_routines=db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.id==db_routine.id).first()
    return db_routines  
@router.delete('/')
def deleteRoutine(db:db_dependency,user:user_dependency,id:int):
    routine=db.query(Routine).filter(Routine.id==id).first()
    
    if routine:
        db.delete(routine)
        db.commit()
       
        
    return routine 
    
       
    

    



    