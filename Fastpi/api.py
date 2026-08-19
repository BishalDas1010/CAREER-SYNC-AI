from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/login")
def login(data: LoginRequest):

    print("Email:", data.email)
    print("Password:", data.password)

    return {
        "message": "Login successful",
        "email": data.email
    }