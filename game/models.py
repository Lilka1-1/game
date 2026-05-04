from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class RoomCreate(BaseModel):
    host_nickname: str
    max_rounds: int = 10
    category: str = "Смешанная"
    timer_seconds: int = 60

class JoinRoom(BaseModel):
    room_code: str
    nickname: str

class PlayerResponse(BaseModel):
    id: int
    nickname: str
    score: int
    is_ready: bool
    is_explaining: bool
    avatar_color: str

class RoomResponse(BaseModel):
    id: int
    code: str
    host_player_id: int
    is_active: bool
    current_round: int
    max_rounds: int
    category: str
    timer_seconds: int
    players: List[PlayerResponse]

class VoteAction(BaseModel):
    word_guessed: bool = False

class GameMessage(BaseModel):
    type: str
    data: dict

class MessageType(str, Enum):
    ROOM_CREATED = "room_created"
    PLAYER_JOINED = "player_joined"
    PLAYER_LEFT = "player_left"
    GAME_STARTING = "game_starting"
    NEW_ROUND = "new_round"
    NEW_PHRASE = "new_phrase"
    VOTE_UPDATE = "vote_update"
    ROUND_END = "round_end"
    GAME_END = "game_end"
    SCORE_UPDATE = "score_update"
    EXPLAINER_CHANGE = "explainer_change"
    TIMER_UPDATE = "timer_update"
    CHAT_MESSAGE = "chat_message"