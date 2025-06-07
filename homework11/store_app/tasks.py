from celery import shared_task
import logging

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)



@shared_task
def add_product(name: str):
    logger.info("Товар '%s' успешно добавлен.", name)