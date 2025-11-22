import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from database import create_document, get_documents, db
from schemas import Profile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Portfolio backend running"}

@app.get("/api/profile", response_model=Profile)
def get_profile():
    # Get the latest profile document
    try:
        docs = get_documents("profile", {}, limit=1)
        if docs:
            doc = docs[-1]
            # Convert Mongo's internal fields
            doc.pop("_id", None)
            return Profile(**doc)
        # Default seed if none exists yet
        return Profile(
            name="Your Name",
            tagline="Teacher • Programmer • Writer • Entrepreneur",
            bio=(
                "I love building things, sharing knowledge, and exploring ideas. "
                "This is my corner of the internet where I collect what I do and what I know."
            ),
            roles=["Teacher", "Programmer", "Writer", "Entrepreneur"],
            skills=["JavaScript", "Python", "React", "FastAPI", "Node.js", "Writing", "Teaching"],
            hobbies=[
                "Running",
                "Working out",
                "Creating fictional worlds",
                "Travelling and sight seeing",
                "Walking around at night",
            ],
            avatar_url=None,
        )
    except Exception as e:
        # If DB not available, still return a sane default to keep UI working
        return Profile(
            name="Your Name",
            tagline="Teacher • Programmer • Writer • Entrepreneur",
            bio=(
                "I love building things, sharing knowledge, and exploring ideas. "
                "This is my corner of the internet where I collect what I do and what I know."
            ),
            roles=["Teacher", "Programmer", "Writer", "Entrepreneur"],
            skills=["JavaScript", "Python", "React", "FastAPI", "Node.js", "Writing", "Teaching"],
            hobbies=[
                "Running",
                "Working out",
                "Creating fictional worlds",
                "Travelling and sight seeing",
                "Walking around at night",
            ],
            avatar_url=None,
        )

class ProfilePayload(BaseModel):
    name: str
    tagline: Optional[str] = None
    bio: Optional[str] = None
    roles: List[str] = []
    skills: List[str] = []
    hobbies: List[str] = []
    avatar_url: Optional[str] = None

@app.post("/api/profile")
async def upsert_profile(payload: ProfilePayload):
    # Save a new profile document (simple create for demo)
    try:
        create_document("profile", payload.model_dump())
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
