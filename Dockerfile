FROM python:3.9
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY dist/*.whl /usr/src/app/
RUN pip install /usr/src/app/*.whl

CMD ["imeiminer"]