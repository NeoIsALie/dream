import logging
import os

import sentry_sdk
import torch
from parlai.core.script import ParlaiPreloadModelScript
from sentry_sdk.integrations.fastapi import FastApiIntegration

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), integrations=[FastApiIntegration()])

cuda = torch.cuda.is_available()
if cuda:
    torch.cuda.set_device(0)  # singe gpu
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

kg_checkpoint_name = os.environ.get("MODEL_CKPT", "1_sent_48_epochs")

logger.info(f"knowledge grounding model {kg_checkpoint_name} is set to run on {device}")

kg_script = ParlaiPreloadModelScript.main(
    task="topical_chat:generator",
    init_model=f"/opt/conda/lib/python3.7/site-packages"
    f"/data/models/topical_chat_blender90_{kg_checkpoint_name}/model.checkpoint",
    model_file=f"/opt/conda/lib/python3.7/site-packages"
    f"/data/models/topical_chat_blender90_{kg_checkpoint_name}/model",
    fp16=False,
    inference="nucleus",
    topp=0.9,
    skip_generation=False,
)

logger.info("knowledge grounding script has loaded the model and is ready")