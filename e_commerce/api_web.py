"""Interface of the application"""
import os
import pickle

from fastapi import FastAPI, HTTPException
import sentry_sdk

from e_commerce.config import get_conf

sentry_sdk.init(
    dsn="https://00cc5017a11b4bc2a393c80dc405696d@o4504119317889024.ingest.sentry.io/4504293165039616",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

app = FastAPI()

with open(
    os.path.join(get_conf().DATA, get_conf().RECOMMENDATION_FILE_NAME[0]), "rb"
) as f:
    recommendations_matrix = pickle.load(f)


@app.get("/")
async def root():
    """Default message"""
    return {
        "message": "for getting recommendations user entrypoint /get-recommendation"
    }


@app.get("/get-recommendation")
async def recommend(client_id: int) -> dict:
    """Returns a list with items recommendations for a client"""

    for user, recommendations in recommendations_matrix:
        if user == client_id:
            return {"recommendations": recommendations}

    raise HTTPException(status_code=404, detail="Id-client not found")
