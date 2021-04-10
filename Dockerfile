FROM python:3.8-slim
RUN mkdir /app
RUN mkdir /app/templates
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py /app/
COPY templates/*.html /app/templates/

ENTRYPOINT ["python"]
CMD ["app.py"]
