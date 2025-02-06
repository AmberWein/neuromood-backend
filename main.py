from fastapi import FastAPI
from controllers.mood_log_controller import router as mood_log_router

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# Include the mood log router
app.include_router(mood_log_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}