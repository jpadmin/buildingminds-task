FROM python:3.8-slim
COPY consumer.py .
RUN pip install kafka-python
CMD ["python", "consumer.py"]
