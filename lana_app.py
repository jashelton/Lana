import tornado.web

from urls import URL_HANDLERS
from tornado.options import options

class LanaApp(tornado.web.Application):
  def __init__(self):

    super(LanaApp, self).__init__(
      handlers=((p, h) for h, patterns in URL_HANDLERS.items() for p in patterns),
      debug=options.debug,
    )