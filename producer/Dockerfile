FROM python:3.8-slim
COPY producer.py .
RUN pip install kafka-python
CMD ["python", "producer.py"]
