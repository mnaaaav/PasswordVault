from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
import sqlite3

app = FastAPI()

# Generate a key (Store it securely in production!)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Database setup
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    encrypted_password TEXT
)
""")
conn.commit()

# Define a Pydantic model for input validation
class PasswordEntry(BaseModel):
    website: str
    username: str
    password: str

@app.post("/store/")
def store_password(entry: PasswordEntry):
    encrypted_password = cipher_suite.encrypt(entry.password.encode())
    cursor.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)",
                   (entry.website, entry.username, encrypted_password))
    conn.commit()
    return {"message": "Password stored securely"}

@app.get("/retrieve/{website}")
def retrieve_password(website: str):
    cursor.execute("SELECT username, encrypted_password FROM passwords WHERE website = ?", (website,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="No password found")
    decrypted_password = cipher_suite.decrypt(result[1]).decode()
    return {"website": website, "username": result[0], "password": decrypted_password}
