from app.handlers.base_handler import BaseHandler
from app.services.ranking_service import RankingService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

# TODO: Eventually, all() should return a list of threads and comments should be retrieved when viewing thread.

@jwtauth
class RankingHandler(BaseHandler):
  ITEMS = ('polls', 'comments', 'threads')
  def get(self, item=None, the_id=None, **kwargs):
    if item == 'polls' and the_id:
      # rankings/:poll_id/poll
      pass
    elif item == 'comments' and the_id:
      # rankings/:comment_id/comment
      pass

  def post(self, item=None, **kwargs):
    self.load_json()
    data = self.request.arguments

    if item == 'polls':
      # rankings/:poll_id/polls
      if data['user_rank'] is not None:
        res = RankingService().update_poll_rank(data)
        response = { 'data': res }
        self.finish(response)
      
      else:
        res = RankingService().add_poll_rank(data)
        response = { 'data': res }
        self.finish(response)

    elif item == 'threads':
      # rankings/:thread_id/threads
      if data['user_rank'] is not None:
        res = RankingService().update_thread_rank(data)
        response = { 'data': res }
        self.finish(response)
      
      else:
        res = RankingService().add_thread_rank(data)
        response = { 'data': res }
        self.finish(response)
    
    # elif item == 'comments':
    #   pass
    #   # rankings/:comment_id/comments
    #   if data['user_rank'] is not None:
    #     res = RankingService().update_comment_rank(data)
    #     response = { 'data': res }
    #     self.finish(response)
      
    #   else:
    #     res = RankingService().add_comment_rank(data)
    #     response = { 'data': res }
    #     self.finish(response)
