import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()

# connecting with the superbase so we need them
SUPABASE_URL = os.environ["VITE_SUPABASE_URL"]


SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = FastAPI()
#add middleware use to communicate the frontend to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# this used for login  and data validation 
class LoginPayload(BaseModel):
    email: str
    password: str

#  this used for login  and data validation 
class ProfileCreate(BaseModel):
    full_name: str = ""
    current_role: str = ""
    education: str = ""
    experience: str = ""
    career_goals: str = ""
# 
class RegisterPayload(BaseModel):
    fullName: str
    email: str
    password: str


# Optional[str] means:
#This variable can either contain a string (str) or None.
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



# the Receive Registraction data from the fortend 
#create the user in superbase Auth
#handle errors and return the user data
@app.post("/api/auth/register")
def register(payload: RegisterPayload):
    #this block is use to Try to create the account
    try:
        #try to sing up in superbase if the user is new
        auth_response = supabase.auth.sign_up({
            #all the data are comming from the frontend 
            "email": payload.email,
            "password": payload.password,
            "options": {
                "data": {
                    "full_name": payload.fullName
                }
            }
        })

    # If registration fails, 
    # check what went wrong and return an appropriate HTTP error to the
    #  frontend
    except Exception as e:
        error = str(e)
        #If Supabase says Too many requests
        if "rate limit" in error.lower():
            raise HTTPException(
                #429 means: Too Many Requests.
                status_code=429,
                detail="Too many verification emails were requested. Please try again later."
            )
        #What if it's NOT a rate-limit error?
        #Invalid email or Invalid details 
        #400 Bad Request
        raise HTTPException(
            status_code=400,
            detail=error
        )
    #Account creation failed, 
    # so stop and send an error to the frontend 
    #“If Supabase didn't return a user after the signup attempt,
    #  something went wrong with account creation.”
    if not auth_response.user:
        raise HTTPException(
            status_code=400,
            detail="Could not create account"
        )


    #After signup, Supabase may give you a session. -> 
    session = auth_response.session

    return {
        "message": "Registration successful",
        "user": {
            "id": auth_response.user.id,
            "email": auth_response.user.email
        },
        #If session exists -> give the access token.
        #If session doesn't exist -> give None.
        "access_token": session.access_token if session else None,
        "refresh_token": session.refresh_token if session else None,
        #“If there is no session, tell the frontend that email confirmation is required.”
        "email_confirmation_required": session is None
    }

 #
@app.post("/api/auth/login")
def login(payload: LoginPayload):
    """
    Single entry point for password login.
    Frontend calls ONLY this endpoint — FastAPI talks to Supabase,
    checks the profile, and tells the frontend exactly where to route.
    """
    try:
        #Here is the user's email and password. Check whether they are correct.
        auth_response = supabase.auth.sign_in_with_password(
            {
                "email": payload.email, 
                "password": payload.password
             }
        )
    # if not then
    except Exception as e:
        # Supabase raises on bad credentials
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
            )

    if not auth_response.session or not auth_response.user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = auth_response.user
    session = auth_response.session
    #User has successfully logged in. Now let's find their profile.
    profile = (
        supabase.table("profiles")
        .select("*")
        #Find the profile belonging to this user
        #.eq() means equals.
        .eq("id", user.id)
        #“I expect zero or one profile.”
        .maybe_single()
        #This actually runs the query against Supabase.
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