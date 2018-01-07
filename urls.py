from app.handlers.auth_handler import AuthHandler
from app.handlers.app_handler import AppHandler

URL_HANDLERS = {
    AuthHandler: (
      r"/(?P<item>{})".format(
        '|'.join(AuthHandler.ITEMS)),
      r"/(?P<item>{})/(?P<token>\d+)"),

    AppHandler: (
      r"/",
    )
}