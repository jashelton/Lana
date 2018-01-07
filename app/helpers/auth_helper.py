import jwt
from sqlalchemy import select
import os

secret_key = os.environ.get('HMAC_SECRET', None)
options = {
  'verify_signature': True,
  'verify_exp': False,
  'verify_nbf': False,
  'verify_iat': True,
  'verify_aud': False
}


def jwtauth(handler_class):
  """Handle Tornado JWT Auth"""
  def wrap_execute(handler_execute):
    def require_auth(handler, kwargs):

      auth = handler.request.headers.get('Authorization')
      if auth:
        # remove Bearer
        auth = auth[7:]
        try:
          token = decode_jwt(auth)
          handler.current_user = token['user_id']

        except Exception as e:
          handler._transforms = []
          handler.write('Authentication Failed')
          handler.set_status(401)
          handler.write(e)
          handler.finish()
      else:
        handler._transforms = []
        handler.write("Missing authorization")
        handler.finish()

      return True

    def _execute(self, transforms, *args, **kwargs):

      try:
        require_auth(self, kwargs)
      except Exception as e:
        # todo: log e
        return False

      return handler_execute(self, transforms, *args, **kwargs)

    return _execute

  handler_class._execute = wrap_execute(handler_class._execute)
  return handler_class

def decode_jwt(token):
  return jwt.decode(
    token,
    secret_key,
    algorithms=['HS256'],
    options=options
  )