import logging

from consumers.rmqconsumer import ReconnectingConsumer

# from multiprocessing import Process


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    amqp_url = "amqp://guest:guest@localhost:5672/%2F"
    consumer = ReconnectingConsumer(amqp_url)
    consumer.run()


if __name__ == "__main__":
    main()
    # Multiprocessing with workers
    # amqp_url = 'amqp://guest:guest@localhost:5672/%2F'
    # consumer = ReconnectingConsumer(amqp_url)
    # consumer_process = Process(target=consumer.run)
    # consumer_process.run()
