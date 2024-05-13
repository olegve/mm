import logging

from celery.app import shared_task


@shared_task()
def received_messages_handler(db_id: int):
    logging.info(f'db_id: {db_id}')
    print(f'Hello from received_messages_handler')


