from django.core.management.base import BaseCommand
from store_app.models import Product, Category
from faker import Faker


class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Start generating test data")
        faker = Faker()
        for _ in range(10):
            category = Category.objects.create(
                name=faker.name(),
                description=faker.sentence(),
            )
            for _ in range(20):
                Product.objects.create(
                    name=faker.sentence(),
                    description=faker.sentence(),
                    price=faker.pydecimal(min_value=0, max_value=1000),
                    category=category,
                )
            self.stdout.write("Продукт создан")

        self.stdout.write("Stop generating test data")
