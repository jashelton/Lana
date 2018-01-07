import json
import tornado.web
from datetime import datetime, date, time, timedelta

import logging
app_log = logging.getLogger("tornado.application")


class BaseHandler(tornado.web.RequestHandler):
  """A class to collect common handler methods - all other handlers should
  subclass this one.
  """

  def set_default_headers(self):
    super().set_default_headers()

    self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
    self.set_header('Access-Control-Allow-Methods', 'HEAD, GET, PUT, POST, DELETE, OPTIONS')
    self.set_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, Origin')

  def load_json(self):
    """Load JSON from the request body and store them in
    self.request.arguments, like Tornado does by default for POSTed form
    parameters.
    If JSON cannot be decoded, raises an HTTPError with status 400.
    """
    try:
      self.request.arguments = json.loads(self.request.body)
    except ValueError:
      msg = "Could not decode JSON: %s" % self.request.body
      app_log.debug(msg)
      raise tornado.web.HTTPError(400, msg)

  def get_json_argument(self, name, default=None):
    """Find and return the argument with key 'name' from JSON request data.
    Similar to Tornado's get_argument() method.
    """
    if default is None:
      default = self._ARG_DEFAULT
    if not self.request.arguments:
      self.load_json()
    if name not in self.request.arguments:
      if default is self._ARG_DEFAULT:
        msg = "Missing argument '%s'" % name
        app_log.debug(msg)
        raise tornado.web.HTTPError(400, msg)
      msg = "Returning default argument {}, as we couldn't find '{}' in {}".format(default, name,
                                                                                   self.request.arguments)
      app_log.debug(msg)
      return default
    arg = self.request.arguments[name]
    app_log.debug("Found '{}': {} in JSON arguments".format(name, arg))
    return arg

  def write(self, chunk):
    # Preprocess any dict because they are automatically converted to json in base class.
    # Conversion in the base class is only for dict.
    if isinstance(chunk, dict):
      chunk = self.pre_json_encoder(chunk)  # convert non-json compatible values
    return super().write(chunk)

  @classmethod
  def pre_json_encoder(cls, val):
    if isinstance(val, (list, tuple, set)):
      return [cls.pre_json_encoder(item) for item in val]
    if isinstance(val, dict):
      return {k: cls.pre_json_encoder(v) for k, v in val.items()}
    if isinstance(val, (date, time, datetime)):
      return val.isoformat()
    if isinstance(val, timedelta):
      return val.total_seconds()
    return val

  def options(self, item=None, the_id=None, *args, **kwargs):
    self.set_status(200)