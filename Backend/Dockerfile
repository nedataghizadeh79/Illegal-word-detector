FROM python:3.9

WORKDIR /back

COPY ./requirements.txt /back/requirements.txt

RUN pip install -r /back/requirements.txt

COPY ./* /back/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
