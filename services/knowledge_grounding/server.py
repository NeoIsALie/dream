import random
import time
from typing import List, Optional

import sentry_sdk
from fastapi import Body, FastAPI
from pydantic import BaseModel

from config import *

app = FastAPI()


class Answer(BaseModel):
    text: str


@app.post('/respond', response_model=Optional[List[Answer]])
def respond(payload: dict = Body(...)):
    batch, history = payload['batch'], payload["batch"][0]
    responses = None
    random.seed(42)
    st_time = time.time()
    if batch:
        user_inputs = {
            "history": history["history"].split("\n") if history["history"] else [""],
            "inputs": [{
                "checked_sentence": sample["checked_sentence"],
                "knowledge": sample["knowledge"],
                "text": sample["text"],
            }
                for sample in batch
            ]
        }
        try:
            raw_responses = kg_script.run(user_inputs)
            responses = [Answer(text=r["text"]) for r in raw_responses]
            logger.info(f"Current sample responses: {responses}")
        except Exception as e:
            sentry_sdk.capture_exception(e)
            logger.exception(e)
    else:
        logger.info("Received empty batch, exiting with empty responses")
    total_time = time.time() - st_time
    logger.info(f"knowledge grounding one batch exec time: {total_time:.3f}s")
    return responses
