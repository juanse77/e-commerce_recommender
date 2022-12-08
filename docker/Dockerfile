FROM python:3.10

RUN pip install https://github.com/juanse77/e-commerce_recommender/releases/download/v1.0.1/e_commerce-1.0.7-py3-none-any.whl

WORKDIR /app/data

ADD data/recommendations.pkl .

WORKDIR /app

CMD uvicorn e_commerce.api_web:app --host 0.0.0.0 --port 8000