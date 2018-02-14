from app.handlers.base_handler import BaseHandler
from app.services.bookmark_service import BookmarkService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

@jwtauth
class BookmarkHandler(BaseHandler):
  def get(self, user_id=None, **kwargs):
    if user_id:
      # bookmarks/:user_id
      res = BookmarkService().bookmarks(user_id)
      response = {'data': res}
      self.finish(response)
    else:
      pass
