from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongodb import db
from app.models.story import StoryCreate, StoryUpdate, StoryInDB
from app.routes.auth import get_current_user
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/story", tags=["Story"])

def to_story_dict(story):
    story["id"] = str(story["_id"])
    del story["_id"]
    return story

@router.post("/create", response_model=StoryInDB)
async def create_story(story: StoryCreate, current_user: dict = Depends(get_current_user)):
    story_data = story.dict()
    story_data["author"] = current_user["username"]
    
    result = await db.stories.insert_one(story_data)
    story_data["id"] = str(result.inserted_id)
    return story_data


@router.get("/", response_model=List[StoryInDB])
async def list_stories():
    stories = await db.stories.find().to_list(100)
    return [to_story_dict(s) for s in stories]


@router.get("/{story_id}", response_model=StoryInDB)
async def get_story(story_id: str):
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return to_story_dict(story)


@router.put("/id/{story_id}", response_model=StoryInDB)
async def update_story(story_id: str, story_update: StoryUpdate, current_user: dict = Depends(get_current_user)):
    
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this story")

    updated = await db.stories.find_one_and_update(
        {"_id": ObjectId(story_id)},
        {"$set": story_update.dict(exclude_unset=True)},
        return_document=True
    )
    return to_story_dict(updated)


@router.delete("/id/{story_id}")
async def delete_story(story_id: str, current_user: dict = Depends(get_current_user)):
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this story")

    await db.stories.delete_one({"_id": ObjectId(story_id)})
    return {"message": "Story deleted"}



# ---- BACKGROUND TASK FTN ----
async def batch_update_countries():
    async for story in db.stories.find({"country": {"$in": [None, ""]}}):
        await db.stories.update_one(
            {"_id": story["_id"]},
            {"$set": {"country": "Unknown"}}
        )
    print("Country field updated in batch")



from fastapi import BackgroundTasks
@router.post("/batch/update-countries")
async def trigger_country_update(
        background_tasks: BackgroundTasks,
        current_user: dict = Depends(get_current_user)
    ):
    background_tasks.add_task(batch_update_countries)
    return {"message": "Background country update started"}


# Periodic Scheduler: setting the periodic country field update every minute
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# scheduler = BackgroundScheduler()

async def update_countries_task():
    print(f"Running batch update for countries at {datetime.now()}")
    await batch_update_countries()

# Set up scheduler
# scheduler = AsyncIOScheduler()
# scheduler.add_job(update_countries_task, 'interval', seconds=60)
# scheduler.start()

