from sqlalchemy import Integer, Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Many-to-many association table
workout_routine_association = Table(
    'workout_association', Base.metadata,
    Column('workout_id', Integer, ForeignKey('workouts.id')),   # 💡 fixed FK targets
    Column('routine_id', Integer, ForeignKey('routines.id'))    # 💡 fixed FK targets
)

class User(Base):
    __tablename__ = 'users'  # ✅ FIXED
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # 💡 Changed from Integer to String
    hashed_password = Column(String)

class Workout(Base):
    __tablename__ = 'workouts'  # ✅ FIXED
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    routines = relationship('Routine', secondary=workout_routine_association, back_populates='workouts')

class Routine(Base):
    __tablename__ = 'routines'  # ✅ FIXED
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    workouts = relationship('Workout', secondary=workout_routine_association, back_populates='routines')
