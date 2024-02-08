from django.core.management.base import BaseCommand
import os
import uuid
from api_crud.utils import random_string
# from wikichat.utils import add_chat_user, customer_chat_topic_fs
# from wizard_dashboard.models import Attorneys
# from manager.models import Member


class Command(BaseCommand):
    help = 'This Custom command is used to backfill attorney as chat user'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--attorney_id', type=str, required=True)

    def handle(self, *args, **options):
        pass
        # try:
        #     attorney = Attorneys.objects.get(uid=options['attorney_id'])
        #     member = Member.objects.filter(user=attorney.user).first()
        #     member.chat_user_id = uuid.uuid4()
        #     member.chat_password = random_string(20)
        #
        #     member.save()
        #     add_chat_user(member)
        #
        #     self.stdout.write(self.style.SUCCESS(
        #         f"Attorney was added to chat user successfully."))
        # except Attorneys.DoesNotExist as e:
        #     self.stdout.write(self.style.ERROR(
        #         f"No Attorney was found with the provided UID: {options['attorney_id']}"))
