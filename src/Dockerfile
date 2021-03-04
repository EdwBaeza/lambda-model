FROM public.ecr.aws/lambda/python:3.6

COPY requirements.txt .
RUN  python3.6 -m pip install --upgrade pip \
    && python3.6 -m pip install -r requirements.txt -t .

COPY app.py .
COPY utils.py .
COPY tmp tmp


# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]