from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Celery, RabbitMQ
from diagrams.programming.framework import Django, Fastapi

with Diagram("All messages scenarios"):
    with Cluster("Event Initiators"):
        admin = Django("Admin")
        frontend = Mobile("Front")
        scheduler = Celery("Scheduler")

    with Cluster("Event API"):
        instant = Fastapi("Instant events")
        instant_ugc = Fastapi("instant events require check")
        automatic = Fastapi("Automatic events")
        event_api = [instant, instant_ugc, automatic]

    with Cluster("Event Queue"):
        instant_ugc_queue = RabbitMQ("UGC queue")
        automatic_queue = RabbitMQ("Automatic queue")
        event_queue = [instant_ugc_queue, automatic_queue]

    with Cluster("Celery Enrichers"):
        instant_enricher = Celery("UGC enricher")
        automatic_enricher = Celery("Automatic enricher")
        enrichers = [instant_enricher]

    with Cluster("Message Queue"):
        instant_message_queue = RabbitMQ("Instant Message Queue")
        instant_ugc_message_queue = RabbitMQ("UGC Message Queue")
        automatic_message_queue = RabbitMQ("Automatic Message Queue")

    with Cluster("Celery Postman"):
        instant_emailer = Celery("Instant Message via channel")
        instant_ugc_emailer = Celery("UGC Message via channel")
        automatic_emailer = Celery("Automatic Message via channel")
        postmans = [instant_emailer, instant_ugc_emailer]

    with Cluster("DBs"):
        notifications_db = Postgresql("Notifications")
        ad_hoc_db = Postgresql("User Data for enrichment")

    end_user = Mobile("End user")

    # admin event
    admin >> Edge(label="event") >> instant
    instant >> Edge(label="get template", style="dotted") >> notifications_db
    instant >> Edge(label="get personal data", style="dotted") >> ad_hoc_db
    instant >> Edge(label="Make and pass message") >> instant_message_queue
    instant_message_queue >> instant_emailer

    # ugc event
    frontend >> Edge(label="event") >> instant_ugc
    instant_ugc >> Edge(label="event") >> instant_ugc_queue
    instant_ugc_queue >> Edge(label="event") >> instant_enricher
    instant_enricher >> Edge(label="make and pass message") >> instant_ugc_message_queue
    instant_message_queue >> Edge(label="message") >> instant_ugc_emailer

    # automatic events
    scheduler >> Edge(label="event") >> automatic
    automatic >> Edge(label="event") >> automatic_queue
    automatic_queue >> Edge(label="event") >> automatic_enricher
    automatic_enricher >> Edge(label="Make and pass message") >> automatic_message_queue
    automatic_message_queue >> Edge(label="message") >> automatic_emailer

    # enrichers
    enrichers >> Edge(label="get template", style="dotted") >> notifications_db
    enrichers >> Edge(label="get personal data", style="dotted") >> ad_hoc_db

    # end
    postmans >> Edge(label="email, messangers") >> end_user
