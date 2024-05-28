from django.core.management.base import BaseCommand

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models.base import ModelBase

MODULE_NAME = "affiliate_partners.factories"

class Command(BaseCommand):
    help = "Create instances of specific model classes based on arguments"

    def create_instances(self, class_name, count=1):
        # Import the module
        module = __import__(MODULE_NAME, fromlist=[class_name])

        # Get the class by name
        try:
            custom_class = getattr(module, class_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(f"Model '{str(module)+class_name}' not found. Check app_label and model_name."))
            return
        custom_class()
        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} instances of '{str(module)+class_name}'."))

    def add_arguments(self, parser):
        parser.add_argument('model_class_name', type=str, help='Name of the model class to create instances of')
        parser.add_argument('--count', type=int, default=1, help='Number of instances to create (default: 1)')

    def handle(self, *args, **kwargs):
        model_class_name = kwargs['model_class_name']
        count = kwargs['count']
        self.create_instances(model_class_name, count)


