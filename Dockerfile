FROM python:3.5.1

EXPOSE 5555

RUN mkdir -p /app
RUN chmod 777 /app
WORKDIR /app
CMD ["make", "run"]

COPY manage.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY Makefile.app ./Makefile
COPY apps ./apps
COPY verbes ./verbes
