# stdlib
import asyncio
import logging
import logging.config
import os

# thirdparty
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from redis.commands.search.indexDefinition import (  # noqa
    IndexDefinition,
    IndexType,
)

# project
from src.monetization_service.api import api_router
from src.monetization_service.queries.temp_metrics import run_query
from src.monetization_service.settings.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info(
        "CONTAINER VERIFICATION "
        "SUCCESSFULLY STARTED WITH VERSION"
        " {}".format(os.getenv("CONTAINER_VERSION"))
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_query, "interval", days=1)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    # redis = get_redis_client()
    #
    # await redis.ft(settings.redis_suggestions_idx_name).dropindex(
    #     delete_documents=True
    # )
    pass


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        log_config=LOGGING_CONFIG,
        use_colors=False,
        port=8000,
    )
