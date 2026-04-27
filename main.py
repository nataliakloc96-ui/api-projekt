from fastapi import FastAPI
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

security = HTTPBearer()

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                password TEXT
                )
""")

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    password: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")



@app.get("/users")
def get_users(user=Depends(verify_token)):
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    users = [dict(row) for row in rows]

    conn.close()
    return {"users": rows}



@app.post("/users")
def add_user(user_data: User, user=Depends(verify_token)):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (user.name, user.age)
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return{"message": "User added",
           "user": {
               "id": user_id,
               "name": user.name,
               "age": user.age
           }}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    if deleted == 0:
        return {"message": "User not found"}
    
    return{"message": f"User {user_id} deleted"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name = ?, age = ? WHERE id = ?",
        (user.name, user.age, user_id)
    )
    conn.commit()

    updated = cursor.rowcount

    conn.close()

    if updated == 0:
        return {"message": "User not found"}
    
    return {
        "message": "User updated",
        "users": {
            "id": user_id,
            "name": user.name,
            "age": user.age
        }

    }

@app.post("/register")
def register(user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (name, age, password) VALUES (?, ?, ?)",
        (user.name, user.age, hashed)
    )
    conn.commit()
    conn.close()

    return{"message": "User registered"}

@app.post("/login")
def login(user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (user.name)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[3]
        if bcrypt.checkpw(user.password.encode(), stored_password):

            token = create_token({"sub": user.name})

            return {"message": "Login successful",
                    "token": token
                    }
    
    return {"message": "Invalid credentials"}

@app.get("/analytics")
def analytics():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT age_group, COUNT(*) FROM users_clean GROUP BY age_group")
    data = cursor.fetchall()

    conn.close()
    return {"analytics": data}

