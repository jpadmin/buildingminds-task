FROM python:3.8-slim
RUN adduser --disabled-password --gecos "" consumer --home /home/consumer/ --uid 1824
WORKDIR /home/consumer/
USER consumer
RUN pip install kafka-python
COPY --chown=consumer:consumer consumer.py .
CMD ["python", "consumer.py"]
