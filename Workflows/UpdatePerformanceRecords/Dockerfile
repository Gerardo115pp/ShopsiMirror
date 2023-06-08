FROM python:3.10.4-alpine3.16
RUN apk add --no-cache gcc musl-dev linux-headers alpine-sdk tzdata
RUN pip install requests prefect pyjwt
RUN pip install schedule bs4 lxml mysql-connector-python==8.0.29

WORKDIR /workflows
COPY . /workflows
RUN mkdir /workflows/incomplete_performance_records
ENV INCOMPLETE_PERFORMANCE_RECORDS_DIR=/workflows/incomplete_performance_records
ENV TZ=America/Mexico_City

ENTRYPOINT [ "/usr/local/bin/python3", "-u", "/workflows/upr_flows.py" ]