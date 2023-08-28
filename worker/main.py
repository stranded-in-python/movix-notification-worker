import logging
from multiprocessing import Process

# from consumers.rmqconsumer import ReconnectingConsumer
# from consumers.workers import AsyncWorker
from consumers.factories import WorkerFactory

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

# def main():
#     # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
#     # amqp_url = "amqp://guest:guest@localhost:5672/%2F"
#     # consumer = ReconnectingConsumer(amqp_url)
#     # consumer.run()
#     worker_factory = WorkerFactory()
#     sendgrid_worker = worker_factory.build_sndrgd_worker(
#         "amqp://guest:guest@localhost:5672/%2F",
#         "hello",
#         "hello"
#     )
#     logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
#     sendgrid_worker.run()


if __name__ == "__main__":
    # main()
    # Multiprocessing with workers
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    worker_factory = WorkerFactory()
    sendgrid_worker = worker_factory.build_sndgrd_worker(
        queue_name="sendgrid",
        routing_key="sendgrid",
    )
    brevo_worker = worker_factory.build_brevo_worker(
        queue_name="brevo", routing_key="brevo"
    )
    process_0 = Process(target=sendgrid_worker.run)
    process_1 = Process(target=brevo_worker.run)
    process_0.start()
    process_1.start()
    process_0.join()
    process_1.join()
