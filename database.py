from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = "sqlite:///./game.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), unique=True, index=True)
    host_player_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    current_round = Column(Integer, default=0)
    max_rounds = Column(Integer, default=10)
    category = Column(String(50), default="Смешанная")
    timer_seconds = Column(Integer, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    players = relationship("Player", back_populates="room", foreign_keys="Player.room_id")
    phrases = relationship("Phrase", back_populates="room")

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50))
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    is_ready = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    is_explaining = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    avatar_color = Column(String(7), default="#4A90D9")
    
    room = relationship("Room", back_populates="players", foreign_keys=[room_id])

class Phrase(Base):
    __tablename__ = "phrases"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(200))
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    round_number = Column(Integer)
    category = Column(String(50), default="Общая")
    difficulty = Column(Integer, default=1)
    is_used = Column(Boolean, default=False)
    
    room = relationship("Room", back_populates="phrases", foreign_keys=[room_id])

class GameState(Base):
    __tablename__ = "game_states"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), unique=True)
    current_word = Column(String(200))
    current_explainer_id = Column(Integer, ForeignKey("players.id"))
    votes = Column(JSON, default={})
    timer_seconds = Column(Integer, default=60)

if os.path.exists("game.db"):
    os.remove("game.db")
    print("🗑️ Старая база данных удалена")

Base.metadata.create_all(bind=engine)
print("✅ База данных создана заново")

def get_db():
    return SessionLocal()

def get_db_depends():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()