# Using python:3.7-slim-buster image
FROM python:3.7-slim-buster
# Defining working directory and copy the requirements file
WORKDIR /usr/src/myapp
COPY requirements.txt .
RUN pip install -U pip setuptools wheel --user
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3","app.py"]