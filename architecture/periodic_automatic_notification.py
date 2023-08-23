from diagrams import Diagram, Edge
from diagrams.oci.monitoring import Email
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Celery, RabbitMQ

with Diagram("Automatic Event", show=False, outformat="png"):
    scheduler = Celery("Scheduler Worker")
    event_templates = Postgresql("Templates db")
    other_dbs = Postgresql("Some other dbs")
    dead_queue = RabbitMQ("Dead Letter Queue") >> other_dbs
    emailer = Email("Worker")

    (
        scheduler
        >> Edge(label="get according template to enrich it", style="dashed")
        >> event_templates
    )
    (
        scheduler
        >> Edge(label="get data for template personalization", style="dashed")
        >> other_dbs
    )

    scheduler >> emailer
    dead_queue >> Edge(label="if retried and did not succeed") >> dead_queue
