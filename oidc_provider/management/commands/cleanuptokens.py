from datetime import timedelta
from django.core.management import BaseCommand
from django.core.management import CommandError
from django.utils import timezone
from oidc_provider.models import Client, Token


class Command(BaseCommand):
    help = 'Cleanup old tokens.'

    def add_arguments(self, parser):
        parser.add_argument('--include', nargs='+', default=[], type=str, help='Include these clients for the cleanup')
        parser.add_argument('--exclude', nargs='+', default=[], type=str, help='Exclude these clients for the cleanup')
        parser.add_argument('--min_age', type=int, required=True,
                            help='Tokens older than min_age are cleaned up. Unit in hours')

    def handle(self, *args, **options):
        excluded = options.get('exclude')
        included = options.get('include')
        min_age = options.get('min_age')

        now = timezone.now()
        threshold = now - timedelta(hours=min_age)

        clients = Client.objects.all()

        if included:
            clients = clients.filter(client_id__in=included)
        if excluded:
            clients = clients.exclude(client_id__in=excluded)

        to_be_deleted = Token.objects.filter(expires_at__lte=threshold, client__in=clients)
        deleted = len(to_be_deleted)
        to_be_deleted.delete()

        self.stdout.write('Deleted {} tokens'.format(deleted))
