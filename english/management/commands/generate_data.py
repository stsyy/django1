from django.core.management.base import BaseCommand

from faker import Faker

from english.models import Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(10):
            Student.objects.create(
                name=fake.name()
            )