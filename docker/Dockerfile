FROM python:3.10

RUN pip install https://github.com/juanse77/e-commerce_recommender/releases/download/v0.6.0/e_commerce-0.6.0-py3-none-any.whl

WORKDIR /app/data

ADD data/recommendations.pkl .

WORKDIR /app

RUN uvicorn e_commerce.api_web:app --host 0.0.0.0 --port 8000