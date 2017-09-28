from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from oidc_provider.lib.utils.token import create_id_token, create_token
from oidc_provider.tests.app.utils import create_fake_client, create_fake_user


class CommandsTest(TestCase):

    def test_creatersakey_output(self):
        out = StringIO()
        call_command('creatersakey', stdout=out)
        self.assertIn('RSA key successfully created', out.getvalue())

    def test_makemigrations_output(self):
        out = StringIO()
        call_command('makemigrations', 'oidc_provider', stdout=out)
        self.assertIn('No changes detected in app', out.getvalue())



class CommandCleanupTokensTest(TestCase):
    def setUp(self):
        self.user = create_fake_user()
        self.client_a = create_fake_client(response_type='code')
        self.client_b = create_fake_client(response_type='code')

        self.age = 12
        now = timezone.now()
        future = now + timedelta(hours=self.age)
        past = now - timedelta(hours=self.age)

        self._create_token(self.client_a, past)
        self._create_token(self.client_a, future)
        self._create_token(self.client_b, past)
        self._create_token(self.client_b, future)

    def _create_token(self, client, expires_at):
        """
        Generate a valid token.
        """
        scope = ['openid', 'email']

        id_token_dic = create_id_token(
            user=self.user,
            aud=client.client_id,
            scope=scope,
        )

        token = create_token(
            user=self.user,
            client=client,
            id_token_dic=id_token_dic,
            scope=scope)
        token.expires_at = expires_at
        token.save()

        return token

    def test_cleanup_tokens_include(self):
        out = StringIO()
        call_command('cleanuptokens', *['--min_age', self.age], include=[self.client_a.client_id], stdout=out)
        self.assertIn('Deleted 1 tokens', out.getvalue())

    def test_cleanup_tokens_exclude(self):
        out = StringIO()
        call_command('cleanuptokens', *['--min_age', self.age], exclude=[self.client_a.client_id], stdout=out)
        self.assertIn('Deleted 1 tokens', out.getvalue())

    def test_cleanup_tokens_all(self):
        out = StringIO()
        call_command('cleanuptokens', *['--min_age', self.age], stdout=out)
        self.assertIn('Deleted 2 tokens', out.getvalue())
