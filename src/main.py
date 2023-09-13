from consumers.factories import CommChannelFactory
from consumers.messagequeue import IncommingMessageQueue


def main():
    factory_comm = CommChannelFactory()
    needed_comm_channels = {
        "email": factory_comm.build_email_channel(),
        # сюда добавляются и другие если есть
    }
    mq = IncommingMessageQueue(needed_comm_channels)
    mq.start_running()


if __name__ == "__main__":
    main()
