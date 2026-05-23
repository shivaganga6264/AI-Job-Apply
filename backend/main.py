import json

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from automation.login import apply_jobs

app = FastAPI()

# Enable CORS
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():

    return {

        "message": "AI Job Auto Apply Backend Running"
    }

# Apply Jobs Route
@app.post("/apply-jobs")
def apply():

    result = apply_jobs()

    return result

# Get History Route
@app.get("/history")
def get_history():

    try:

        with open(
            "backend/history.json",
            "r"
        ) as file:

            history = json.load(file)

    except:

        history = []

    return history