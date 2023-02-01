import random
import time

import sentry_sdk
from flask import Flask, request, jsonify

from config import *

app = Flask(__name__)


@app.route("/respond", methods=["POST"])
def respond():
    batch = request.json["batch"]
    responses = [""]
    random.seed(42)
    st_time = time.time()
    if batch:
        user_inputs = {"history": batch[0]["history"].split("\n") if batch[0]["history"] else [""], "inputs": []}
        for sample in batch:
            user_inputs["inputs"].append(
                {
                    "checked_sentence": sample["checked_sentence"],
                    "knowledge": sample["knowledge"],
                    "text": sample["text"],
                }
            )
        try:
            raw_responses = kg_script.run(user_inputs)
            responses = [r["text"] for r in raw_responses]
            logger.info(f"Current sample responses: {responses}")
        except Exception as e:
            sentry_sdk.capture_exception(e)
            logger.exception(e)
    else:
        logger.info("Received empty batch, exiting with empty responses")
    total_time = time.time() - st_time
    logger.info(f"knowledge grounding one batch exec time: {total_time:.3f}s")
    return jsonify(responses)
