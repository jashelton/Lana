from app.handlers.base_handler import BaseHandler
from app.services.follows_service import FollowsService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

@jwtauth
class FollowsHandler(BaseHandler):
  def get(self, user_id=None, **kwargs):
    pass

  def post(self, user_id):
    self.load_json()
    data = self.request.arguments
    
    res = FollowsService().follow_user(user_id, data)
    response = { 'data': res }
    self.finish(response)

  def delete(self, user_id):
    self.load_json()
    data = self.request.arguments

    res = FollowsService().unfollow_user(user_id, data)
    response = { 'data': res }
    self.finish(response)
    