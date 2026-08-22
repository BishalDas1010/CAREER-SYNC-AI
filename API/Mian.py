import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ["VITE_SUPABASE_URL"]


SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginPayload(BaseModel):
    email: str
    password: str


class ProfileCreate(BaseModel):
    full_name: str = ""
    current_role: str = ""
    education: str = ""
    experience: str = ""
    career_goals: str = ""

def get_user_from_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )

    token = authorization.split(" ", 1)[1]

    try:
        response = supabase.auth.get_user(token)

        if not response.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return response.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


class RegisterPayload(BaseModel):
    fullName: str
    email: str
    password: str


@app.post("/api/auth/register")
def register(payload: RegisterPayload):

    try:
        auth_response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password,
            "options": {
                "data": {
                    "full_name": payload.fullName
                }
            }
        })

    except Exception as e:
        error = str(e)

        if "rate limit" in error.lower():
            raise HTTPException(
                status_code=429,
                detail="Too many verification emails were requested. Please try again later."
            )

        raise HTTPException(
            status_code=400,
            detail=error
        )

    if not auth_response.user:
        raise HTTPException(
            status_code=400,
            detail="Could not create account"
        )

    session = auth_response.session

    return {
        "message": "Registration successful",
        "user": {
            "id": auth_response.user.id,
            "email": auth_response.user.email
        },
        "access_token": session.access_token if session else None,
        "refresh_token": session.refresh_token if session else None,
        "email_confirmation_required": session is None
    }
 
@app.post("/api/auth/login")
def login(payload: LoginPayload):
    """
    Single entry point for password login.
    Frontend calls ONLY this endpoint — FastAPI talks to Supabase,
    checks the profile, and tells the frontend exactly where to route.
    """
    try:
        auth_response = supabase.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as e:
        # Supabase raises on bad credentials
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not auth_response.session or not auth_response.user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = auth_response.user
    session = auth_response.session

    profile = (
        supabase.table("profiles")
        .select("*")
        .eq("id", user.id)
        .maybe_single()
        .execute()
    )

    return {
        "profile_exists": profile.data is not None,
        "user": {"id": user.id, "email": user.email},
        "profile": profile.data,
        # frontend needs these to keep the supabase-js client in sync
        # (e.g. for the OAuth button, or any authenticated calls it makes later)
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
    }