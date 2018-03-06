from app.handlers.base_handler import BaseHandler
from app.services.comments_service import CommentsService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

# TODO: Eventually, all() should return a list of threads and comments should be retrieved when viewing thread.

@jwtauth
class CommentsHandler(BaseHandler):
  ITEMS = ('comments', 'threads')
  def get(self, item=None, the_id=None, **kwargs):
    print(item)
    if item == 'threads' and the_id:
      # threads/:poll_id
      res = CommentsService().get_threads_by_poll(the_id)
      response = {'data': res}
      self.finish(response)
    elif item == 'comments' and the_id:
      # comments/:thread_id
      res = CommentsService().get_comments_by_thread(the_id)
      response = {'data': res}
      self.finish(response)

  def post(self, data=None, **kwargs):
    if data:
      return