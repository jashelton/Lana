from app.handlers.base_handler import BaseHandler
from app.services.follows_service import FollowsService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

@jwtauth
class FollowsHandler(BaseHandler):
  def get(self, user_id=None, **kwargs):
    print(user_id)