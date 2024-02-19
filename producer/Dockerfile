FROM python:3.8-slim
RUN adduser --disabled-password --gecos "" producer --home /home/producer/ --uid 1824
WORKDIR /home/producer/
USER producer
RUN pip install kafka-python
COPY --chown=producer:producer producer.py .
CMD ["python", "producer.py"]
