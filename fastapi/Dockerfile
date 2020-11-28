FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./ /app
COPY ./dublinbus-28165-firebase-adminsdk-43ti1-05d276db4d.json /firebase_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS /firebase_key.json
