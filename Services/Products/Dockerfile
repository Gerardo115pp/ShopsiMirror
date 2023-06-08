FROM python:3.10.4-alpine3.16
RUN pip install requests Flask Flask-Cors openpyxl==3.0.10 mysql-connector-python==8.0.29 pyjwt bs4 lxml flask-sock redis

WORKDIR /app
COPY . /app
RUN mkdir /app/static
RUN mkdir /app/excel_sheets
RUN mkdir /app/Config/tokens
EXPOSE 4500

ENTRYPOINT [ "/usr/local/bin/python3", "-u", "/app/start.py" ]