FROM python:3.12-alpine3.18

WORKDIR /kssspace

COPY ./requirements.base.txt /kssspace/requirements.base.txt

RUN pip install --no-cache-dir --upgrade -r requirements.base.txt

COPY ./instance/config /kssspace/instance/config
COPY ./kssspace /kssspace/kssspace

EXPOSE 5000

CMD ["hypercorn", "kssspace.main:create_app()", "--bind", "0.0.0.0:5000"]