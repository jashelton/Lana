from app.handlers.base_handler import BaseHandler
from app.models.auth import Auth
# from app.helpers.auth_helper import decode_jwt
from app.services.auth_service import AuthService
import jwt
from app.models.errors import HTTPError
import os
import urllib.parse

SECRET = os.environ.get('HMAC_SECRET', None)


class AuthHandler(BaseHandler):
  ITEMS = ('login', 'logout', 'register')

  def get(self, item=None):
    self.write('<html><body><form action="/login" method="post">'
               'email_address: <input type="text" name="email_address">'
               'password: <input type="text" name="password">'
               '<input type="submit" value="Sign in">'
               '</form></body></html>')

  def post(self, item=None, token=None):
    self.load_json()
    data = self.request.arguments
    response = {}
    if token:
      pass
    elif item == 'login':
      # do /login
      # TODO: email is actually username right now.  TBD on how this will be handled in the future.
      email = data["username"]
      password = data["password"]
      auth = Auth(email, password)
      if auth.login():
        encoded = jwt.encode({
          'user_id': auth.user},
          # 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
          SECRET,
          algorithm='HS256'
        )
        self.set_cookie("token", str(encoded)[2:-1])
        # auth.record_login(ip=self.request.remote_ip)
        # [2:-1] is removing b'' from token
        response = {'token': str(encoded)[2:-1], 'current_user': {'username': auth.email, 'id': auth.user}}
      else:
        raise HTTPError(reason="Login failed")
    elif item == "logout":
      # TODO: test this
      self.clear_cookie("token")
      self.set_status(200)
      response = {'message': 'Successfully logged out user'}
    elif item == "register":
      form_data = data['data']
      user_info = dict(name=form_data['name'], username=form_data['username'], password=form_data['password'])
      res = AuthService().register(user_info)
      response = { 'data': res }
    else:
      assert item not in self.ITEMS, 'Not implemented: item={}'.format(item)
      raise HTTPError(404)
    self.finish(response)