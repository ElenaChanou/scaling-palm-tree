"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Practice teamwork, conditioning, and soccer skills",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "ava@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Develop basketball fundamentals and play competitive games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and creative visual expression",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["sarah@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, perform, and build confidence through theater",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["nora@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Club": {
        "description": "Practice public speaking, argumentation, and critical thinking",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build robots and solve engineering challenges together",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["henry@mergington.edu", "chloe@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Improve serving, teamwork, and competitive volleyball play",
        "schedule": "Mondays and Wednesdays, 4:30 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["grace@mergington.edu", "jack@mergington.edu"]
    },
    "Track & Field Club": {
        "description": "Train for running, jumping, and relay events throughout the season",
        "schedule": "Tuesdays and Thursdays, 3:45 PM - 5:15 PM",
        "max_participants": 20,
        "participants": ["zoe@mergington.edu", "owen@mergington.edu"]
    },
    "Ceramics Club": {
        "description": "Explore clay sculpting, pottery techniques, and glazing methods",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["lily@mergington.edu", "mason@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn composition, lighting, and digital editing through creative projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "leah@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve challenging problems and prepare for mathematics competitions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["noah@mergington.edu", "ella@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments, explore STEM topics, and build scientific curiosity",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["benjamin@mergington.edu", "harper@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

   # Validate student is not already signed up 
    if email in activity["participants"]:
          raise HTTPException(status_code=400, detail="Student already signed up for this activity")    

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Remove the student if present
    try:
        activity["participants"].remove(email)
    except ValueError:
        raise HTTPException(status_code=404, detail="Participant not found")

    return {"message": f"Unregistered {email} from {activity_name}"}
