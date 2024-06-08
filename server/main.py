from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Models
class User(BaseModel):
    username: str

class Message(BaseModel):
    sender: str
    receiver: str
    content: str

class Chat(BaseModel):
    users: List[User]
    messages: List[Message]

# In-memory storage
chat_db = Chat(users=[], messages=[])

# Routes
@app.post("/users/", response_model=User)
def create_user(user: User):
    if any(u.username == user.username for u in chat_db.users):
        raise HTTPException(status_code=400, detail="Username already exists")
    chat_db.users.append(user)
    return user

@app.post("/messages/", response_model=Message)
def send_message(message: Message):
    if not any(u.username == message.sender for u in chat_db.users) or \
       not any(u.username == message.receiver for u in chat_db.users):
        raise HTTPException(status_code=404, detail="Sender or receiver not found")
    chat_db.messages.append(message)
    return message

@app.get("/messages/{username}", response_model=List[Message])
def get_messages(username: str):
    if not any(u.username == username for u in chat_db.users):
        raise HTTPException(status_code=404, detail="User not found")
    user_messages = [m for m in chat_db.messages if m.sender == username or m.receiver == username]
    return user_messages

# Run with: uvicorn main:app --reload
