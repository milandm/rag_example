from django.core.management.base import BaseCommand
from oauth2_provider.models import get_application_model

class Command(BaseCommand):
    help = 'Create OAuth2 Application'

    def handle(self, *args, **kwargs):
        Application = get_application_model()
        app = Application.objects.create(
            client_id="your-client-id",
            client_secret="your-client-secret",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            name="Your Application Name"
        )
        self.stdout.write(self.style.SUCCESS(f"Created OAuth2 Application: {app.name}"))


# from oauth2_provider.models import get_application_model
#
# Application = get_application_model()
# app = Application.objects.create(
#     client_id="your-client-id",
#     client_secret="your-client-secret",
#     client_type=Application.CLIENT_CONFIDENTIAL,  # or Application.CLIENT_PUBLIC
#     authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,  # or other grant types
#     name="Your OAuth2 App",
#     redirect_uris="http://localhost:8000/callback/",  # For Authorization Code or Implicit
# )
#
# print(f"Created OAuth2 Application: {app.name}")

client_id = "Aa2nr1GO4lw2odQq1Ikpi7YNixqFFmfnsWE7F6JU"
client_secret = "pbkdf2_sha256$600000$TUoZPIQrG9L25QGwsUxGqU$0+ziDvapmzxABwxIV3vW6apGNw60wX177tv4TuW/Ug4="