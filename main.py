from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel

app = FastAPI()

# Database connection
def get_db():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    return conn, cursor

# Ensure tables exist
def create_tables():
    conn, cursor = get_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT, 
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

create_tables()  # Run on startup

# Pydantic models for input validation
class User(BaseModel):
    username: str
    password: str

class PasswordEntry(BaseModel):
    website: str
    username: str
    password: str

# User Registration
@app.post("/register")
def register(user: User):
    conn, cursor = get_db()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
        return {"message": "User registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()

# User Login
@app.post("/login")
def login(user: User):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials or user not registered")

# Store a password
@app.post("/store")
def store_password(entry: PasswordEntry):
    conn, cursor = get_db()
    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", 
                   (entry.website, entry.username, entry.password))
    conn.commit()
    conn.close()
    return {"message": "Password stored successfully"}

# Retrieve all stored passwords
@app.get("/retrieve")
def retrieve_passwords():
    conn, cursor = get_db()
    cursor.execute("SELECT website, username, password FROM passwords")
    data = cursor.fetchall()
    conn.close()
    
    return {"passwords": [{"website": row[0], "username": row[1], "password": row[2]} for row in data]}
