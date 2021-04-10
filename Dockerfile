FROM python:3.8-slim
RUN mkdir /app
RUN mkdir /app/templates
RUN mkdir /app/static
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py /app/
COPY templates/* /app/templates/
COPY static/* /app/static/

ENTRYPOINT ["python"]
CMD ["app.py"]
