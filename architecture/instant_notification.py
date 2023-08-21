from diagrams import Diagram, Edge
from diagrams.oci.monitoring import Email
from diagrams.programming.framework import Django, Fastapi

# ручная отправка рассылки менеджером
with Diagram("One-time notification", show=False, outformat="png"):
    event = Django("Manager's admin")
    event_api = Fastapi("Event API")
    worker = Email("Worker")

    event >> Edge(label="event") >> event_api >> worker

    # здесь используются rabbit mq и две базы
    # (одна - для содержания оповещения,
    # другая - для истории отправления) ? Я запутался
