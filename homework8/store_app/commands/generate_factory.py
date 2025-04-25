from django.core.management.base import BaseCommand
from store_app.factories import ProductFactory


class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Start generating Product")

        products = ProductFactory.create_batch(10)

        self.stdout.write("Stop generating Product")
