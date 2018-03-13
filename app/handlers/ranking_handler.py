from app.handlers.base_handler import BaseHandler
from app.services.ranking_service import RankingService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

# TODO: Eventually, all() should return a list of threads and comments should be retrieved when viewing thread.

@jwtauth
class RankingHandler(BaseHandler):
  ITEMS = ('polls', 'comments')
  def get(self, item=None, the_id=None, **kwargs):
    if item == 'polls' and the_id:
      # rankings/:poll_id/poll
      pass
      # res = RankingService().get_ranking_by_poll(the_id)
      # response = {'data': res}
      # self.finish(response)
    elif item == 'comments' and the_id:
      # rankings/:comment_id/comment
      pass
      # res = RankingService().get_ranking_by_comment(the_id)
      # response = {'data': res}
      # self.finish(response)

  # def post(self, item=None, **kwargs):
  #   self.load_json()
  #   data = self.request.arguments

  #   if item == 'comments':
  #     res = CommentsService().add_comment(data['commentData'])
  #     response = {'data': res}
  #     self.finish(response)
  #   elif item == 'threads':
  #     res = CommentsService().add_thread(data['threadData'])
  #     response = {'data': res}
  #     self.finish(response)

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

    elif item == 'comments':
      # rankings/:comment_id/comment
      pass
