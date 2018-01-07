from tornado.web import HTTPError

class InvalidParametersError(HTTPError):
  def __init__(self, status_code=422, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class InvalidTokenError(HTTPError):
  def __init__(self, status_code=400, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class NoTokenProvided(HTTPError):
  def __init__(self, status_code=400, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class ResourceNotFoundError(HTTPError):
  def __init__(self, status_code=404, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class UnauthorizedRequest(HTTPError):
  def __init__(self, status_code=401, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class UserNotFoundError(HTTPError):
  def __init__(self, status_code=401, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class ArgumentError(HTTPError):
  def __init__(self, status_code=400, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')

class PasswordComplexityError(HTTPError):
  def __init__(self, status_code=400, log_message=None, *args, **kwargs):
    self.status_code = status_code
    self.log_message = log_message
    self.args = args
    self.reason = kwargs.get('reason', None)
    if log_message and not args:
      self.log_message = log_message.replace('%', '%%')