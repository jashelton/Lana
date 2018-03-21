from app.handlers.base_handler import BaseHandler
from app.services.poll_service import PollService
from app.helpers.auth_helper import jwtauth
# from app.models.errors import HTTPError

@jwtauth
class PollsHandler(BaseHandler):
  ITEMS = ('polls')
  def get(self, item=None, user=None, current_user=None, **kwargs):
    if user:
      # polls/:user
      res = PollService().get_poll_by_user(user, current_user)
      response = {'data': res}
      self.finish(response)
    else:
      self.finish({'error': 'blah'})

  def post(self, data=None, **kwargs):
    if data:
      return