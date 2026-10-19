from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal, engine
import models

# Создаём таблицы в базе (если их нет)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость для получения сессии базы
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Схемы данных для валидации
class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None  # <- вот тут изменили

class HabitResponse(HabitCreate):
    id: int
    is_completed_today: bool
    class Config:
        from_attributes = True

# --- Эндпоинты ---

@app.get("/")
def read_root():
    return {"message": "HabitFlow API работает!"}

@app.get("/habits", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    # Временно берём все привычки (в реальности фильтровали бы по пользователю)
    return db.query(models.Habit).all()

@app.post("/habits", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = models.Habit(title=habit.title, description=habit.description)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@app.put("/habits/{habit_id}/complete", response_model=HabitResponse)
def toggle_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Привычка не найдена")
    db_habit.is_completed_today = not db_habit.is_completed_today
    db.commit()
    db.refresh(db_habit)
    return db_habit