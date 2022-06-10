# Build
FROM python:3.9 AS build-image
WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app
RUN pip install tox
COPY . /usr/src/app
RUN tox -e build


# Final image
FROM python:3.9
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY --from=build-image /usr/src/app/dist/*.whl /usr/src/app/
RUN pip install /usr/src/app/*.whl

CMD ["imeiminer"]