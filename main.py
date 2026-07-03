from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

API_KEY = "ak_ez9z451rm8dkgsqf46wvh645"
EMAIL = "25f1001984@ds.study.iitm.ac.in"

app = FastAPI()

# Allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class RequestBody(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    body: RequestBody,
    x_api_key: str = Header(default=None)
):
    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = body.events

    total_events = len(events)
    unique_users = len(set(e.user for e in events))

    revenue = 0.0
    user_totals = {}

    for e in events:
        if e.amount > 0:
            revenue += e.amount
            user_totals[e.user] = user_totals.get(e.user, 0) + e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }
