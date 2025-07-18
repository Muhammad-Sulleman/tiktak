from fastapi import APIRouter ,status ,HTTPException
from typing import Optional
from pydantic import BaseModel
from api.models import Workout
from api.deps import db_dependency ,user_dependency
router=APIRouter(
    prefix="/workouts",
    tags=["workouts"]
)
class WorkoutBase(BaseModel):
    name :str
     
    description:Optional[str]=None

class WorkoutCreate(WorkoutBase):
    pass
@router.get("/")    
def get_workout(db:db_dependency,user:user_dependency,workout_id):
    return db.query(Workout).filter(Workout.id==workout_id).first()
@router.get('/workouts')
def get_workouts(db:db_dependency,user:user_dependency):
    return db.query(Workout).all()

@router.post("/")
def create_workout(db:db_dependency,user:user_dependency,workout:WorkoutCreate):
    db_workout=Workout(**workout.model_dump(),user_id=user.get('id'))
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.delete("/")
def delete_workout(db:db_dependency,user_dependency,workout_id):
    workout=db.query(Workout).filter(Workout.id==workout_id)
    if workout:
        db.delete(workout)
        db.commit()
        
    return workout

    