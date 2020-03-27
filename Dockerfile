FROM python:3.7-alpine

ENV TZ 'Asia/Tehran'
RUN apk update && apk add tzdata libpq postgresql-dev build-base
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev && \
    cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo $TZ > /etc/timezone
RUN apk add --update --no-cache g++ gcc libxslt-dev


WORKDIR /bot_root

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./
CMD ["python", "main.py"]
ENV PYTHONPATH /bot_root