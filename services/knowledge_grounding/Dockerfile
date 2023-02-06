FROM pytorch/pytorch:1.5-cuda10.1-cudnn7-runtime

ARG MODEL_CKPT

ENV MODEL_CKPT ${MODEL_CKPT}

ARG DATA_ARG
ARG MODEL1_ARG
ARG MODEL2_ARG

RUN apt-get update && apt-get install -y --allow-unauthenticated git wget && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY . /src

RUN pip install -r /src/requirements.txt &&\
    pip install git+https://github.com/Saraharas/ParlAI@v0.9.4-kg-batch-2models#egg=ParlAI &&\
    python -c "import nltk; nltk.download('punkt')"

# create dirs for data and models
RUN mkdir -p /opt/conda/lib/python3.7/site-packages/data/models

#load data
RUN wget $DATA_ARG -q -P /opt/conda/lib/python3.7/site-packages/data &&\
tar -xvzf /opt/conda/lib/python3.7/site-packages/data/*.tar.gz -C /opt/conda/lib/python3.7/site-packages/data &&\
rm /opt/conda/lib/python3.7/site-packages/data/*.tar.gz &&\
wget $MODEL1_ARG -q -P /opt/conda/lib/python3.7/site-packages/data/models &&\
tar -xvzf /opt/conda/lib/python3.7/site-packages/data/models/*.tar.gz -C /opt/conda/lib/python3.7/site-packages/data/models &&\
rm /opt/conda/lib/python3.7/site-packages/data/models/*.tar.gz &&\
wget $MODEL2_ARG -q -P /opt/conda/lib/python3.7/site-packages/data/models &&\
tar -xvzf /opt/conda/lib/python3.7/site-packages/data/models/*.tar.gz -C /opt/conda/lib/python3.7/site-packages/data/models &&\
rm /opt/conda/lib/python3.7/site-packages/data/models/*.tar.gz


CMD uvicorn --workers=1 server:app --host=0.0.0.0 --port=8083 --reload
