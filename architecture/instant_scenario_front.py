from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Mobile
from diagrams.oci.monitoring import Email
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Celery, RabbitMQ
from diagrams.programming.framework import Fastapi

# ручная отправка рассылки менеджером
with Diagram("Instant Event Front", show=False, outformat="png"):
    manager = Mobile("Frontend")
    event_api = Fastapi("Event API endpoint (Producer)")

    queue = RabbitMQ("Queue for instant events")

    with Cluster("Worker"):
        inst_worker = Celery("Worker (Consumer)")
        emailer = Email("Worker")

    event_templates = Postgresql("Templates db")
    other_dbs = Postgresql("Some other dbs")
    dead_queue = RabbitMQ("Dead Letter Queue")

    manager >> Edge(label="event") >> event_api >> Edge(label="event") >> queue
    queue >> Edge(label="event") >> inst_worker
    (
        inst_worker
        >> Edge(label="get according template to enrich it", style="dashed")
        >> event_templates
    )
    inst_worker >> Edge(label="if did not email lately") >> emailer
    emailer >> Edge(label="if retried and did not succeed") >> dead_queue
    (
        inst_worker
        >> Edge(label="get data for template personalization", style="dashed")
        >> other_dbs
    )
