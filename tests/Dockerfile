FROM python:3.6

WORKDIR /app

COPY src/requirements.txt src/
RUN  python -m pip install --upgrade pip \
    && python -m pip install -r src/requirements.txt -t .

COPY src/utils.py src/
COPY src/app.py src/
COPY src/tmp src/tmp

COPY tests/unit tests/unit
RUN pip install pytest pytest-mock --user 
