from oidc_provider.lib.utils.token import create_token


def default_userinfo(claims, user):
    """
    Default function for setting OIDC_USERINFO.
    `claims` is a dict that contains all the OIDC standard claims.
    """
    return claims


def default_sub_generator(user):
    """
    Default function for setting OIDC_IDTOKEN_SUB_GENERATOR.
    """
    return str(user.id)


def default_after_userlogin_hook(request, user, client):
    """
    Default function for setting OIDC_AFTER_USERLOGIN_HOOK.
    """
    return None


def default_after_end_session_hook(request, id_token=None, post_logout_redirect_uri=None, state=None, client=None, next_page=None):
    """
    Default function for setting OIDC_AFTER_END_SESSION_HOOK.

    :param request: Django request object
    :type request: django.http.HttpRequest

    :param id_token: token passed by `id_token_hint` url query param - do NOT trust this param or validate token
    :type id_token: str

    :param post_logout_redirect_uri: redirect url from url query param - do NOT trust this param
    :type post_logout_redirect_uri: str

    :param state: state param from url query params
    :type state: str

    :param client: If id_token has `aud` param and associated Client exists, this is an instance of it - do NOT trust this param
    :type client: oidc_provider.models.Client

    :param next_page: calculated next_page redirection target
    :type next_page: str
    :return:
    """
    return None


def default_idtoken_processing_hook(id_token, user):
    """
    Hook to perform some additional actions ti `id_token` dictionary just before serialization.

    :param id_token: dictionary contains values that going to be serialized into `id_token`
    :type id_token: dict

    :param user: user for whom id_token is generated
    :type user: User

    :return: custom modified dictionary of values for `id_token`
    :rtype dict
    """
    return id_token


def default_create_token(user, client, scope, id_token_dic=None):
    """
    Default function for setting OIDC_CREATE_TOKEN
    :param user:
    :param client:
    :param scope:
    :param id_token_dic:
    :return:
    """
    return create_token(user, client, scope, id_token_dic)