# Communicational workers

## What is this?

This is the consumer for RabbitMQ which sends notifications to users via specified communicational channel.

## What does it do?

It gets a message from RabbitMQ and tries to send it to user(s) using proper communicational channel. If the message can not be delivered it goes to Dead Letter Queue.
The message comsumed up to 3 times (it is configured by env). If it consumed for the 4th time it gets out of a queue.

## How do I use it?

Set up proper producer for the durable queue and send the message using the according format. The worker would get the UUID of the template from database,
validate, render it and send to user(s).

## What is under the hood?

    - Broker: RabbitMQ
    - Broker library: aio_pika
    - Template storage: PSQL
    - Template render: jinja2

## Authors

[Movix](https://github.com/stranded-in-python)
