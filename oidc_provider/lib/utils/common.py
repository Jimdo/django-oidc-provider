from hashlib import sha224

from django.core.urlresolvers import reverse
from django.http import HttpResponse

from oidc_provider import settings

try:
    from urlparse import urlsplit, urlunsplit
except ImportError:
    from urllib.parse import urlsplit, urlunsplit


def cleanup_url_from_query_string(uri):
    """
    Function used to clean up the uri from any query string, used i.e. by endpoints to validate redirect_uri

    :param uri: URI to clean from query string
    :type uri: str
    :return: cleaned URI without query string
    """
    clean_uri = urlsplit(uri)
    clean_uri = urlunsplit(clean_uri._replace(query=''))
    return clean_uri


def redirect(uri):
    """
    Custom Response object for redirecting to a Non-HTTP url scheme.
    """
    response = HttpResponse('', status=302)
    response['Location'] = uri
    return response


def get_site_url(site_url=None, request=None):
    """
    Construct the site url.

    Orders to decide site url:
        1. valid `site_url` parameter
        2. valid `SITE_URL` in settings
        3. construct from `request` object
    """
    site_url = site_url or settings.get('SITE_URL')
    if site_url:
        return site_url
    elif request:
        return '{}://{}'.format(request.scheme, request.get_host())
    else:
        raise Exception('Either pass `site_url`, '
                        'or set `SITE_URL` in settings, '
                        'or pass `request` object.')


def get_issuer(site_url=None, request=None):
    """
    Construct the issuer full url. Basically is the site url with some path
    appended.
    """
    site_url = get_site_url(site_url=site_url, request=request)
    path = reverse('oidc_provider:provider-info') \
        .split('/.well-known/openid-configuration')[0]
    issuer = site_url + path

    return str(issuer)


def get_browser_state_or_default(request):
    """
    Determine value to use as session state.
    """
    key = request.session.session_key or settings.get('OIDC_UNAUTHENTICATED_SESSION_MANAGEMENT_KEY')
    return sha224(key.encode('utf-8')).hexdigest()


