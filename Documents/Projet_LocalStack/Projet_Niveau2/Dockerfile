FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install flask \
flask_sqlalchemy \
flask_jwt_extended \
werkzeug \
boto3

EXPOSE 5000

CMD ["python", "app.py"]
