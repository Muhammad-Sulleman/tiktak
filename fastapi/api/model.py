from sqlalchemy import Integer ,Column,String ,ForeignKey,Table
from sqlalchemy.orm import relationship
from .database import Base
workout_routine_association=Table(
    'workout_association',Base.metadata,
    Column('workout_id',Integer,ForeignKey('workout_id')),
    Column('routine_id',Integer,ForeignKey('routine_id'))
    
)
class User(Base):
    __table_name='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(Integer,unique=True,index=True)
    hashed_password=Column(String)
    
class Workout(Base):
    __table_name='workouts'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    name=Column(String,index=True)
    description=Column(String,index=True)
    routines=relationship('Routine',secondary=workout_routine_association,back_populates='workouts')
    
class Routine(Base):
    __table_name='routines'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    name=Column(String,index=True)
    description=Column(String,index=True)
    workouts=relationship('Workout',secondary=workout_routine_association,back_populates='Routine')
