import logging
import time
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from ml_pipeline.pipeline.ml_pipeline import run_ml_pipeline
from rag_pipeline.rag.rag_pipeline import run_rag_pipeline
from ml_to_rag_bridge import build_rag_user_data

from fastapi.middleware.cors import CORSMiddleware


# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("ergocare-api")


# FastAPI Setup
app = FastAPI(title="ErgoCare AI API", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SurveyInput(BaseModel):
    data: Dict[str, Any]


@app.get("/")
def root():
    return {"status": "ok", "service": "ErgoCare AI API"}


@app.post("/predict")
def predict(payload: SurveyInput):
    start = time.time()
    logger.info("/predict request received")

    ml_output = run_ml_pipeline(payload.data)

    elapsed = time.time() - start
    logger.info(f"/predict completed in {elapsed:.2f}s")

    return ml_output


@app.post("/report")
def report(payload: SurveyInput):
    start = time.time()
    logger.info("/report request received")

    # ML pipeline
    logger.info("Running ML pipeline...")
    ml_output = run_ml_pipeline(payload.data)

    # Adapter
    logger.info("Converting ML output -> RAG user format...")
    rag_user_data = build_rag_user_data(ml_output)

    # RAG pipeline
    logger.info("Running RAG pipeline...")
    rag_report = run_rag_pipeline(rag_user_data)

    elapsed = time.time() - start
    logger.info(f"/report completed in {elapsed:.2f}s")

    return {
        "ml_output": ml_output,
        "rag_user_data": rag_user_data,
        "rag_report": rag_report
    }
