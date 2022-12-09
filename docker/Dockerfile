FROM python:3.10

ARG version

RUN pip install https://github.com/juanse77/e-commerce_recommender/releases/download/v$version/e_commerce-$version-py3-none-any.whl

WORKDIR /app/data

ADD data/recommendations.pkl .

WORKDIR /app

CMD uvicorn e_commerce.api_web:app --host 0.0.0.0 --port 8000