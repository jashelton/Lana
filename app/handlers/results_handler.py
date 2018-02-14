from app.handlers.base_handler import BaseHandler
from app.services.results_service import ResultsService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

@jwtauth
class ResultsHandler(BaseHandler):
  def get(self, the_id=None, **kwargs):
    if the_id:
      # results/:id
      res = ResultsService().get_results_by_poll_id(the_id)
      response = { 'data': res }

      self.finish(response)
    else:
      data = dict(
        poll_id = self.get_argument('poll_id', None),
        user_id = self.get_argument('user_id', None),
        filters = self.get_argument('filters', None).split(',')
      )

      res = ResultsService().update_poll_filters(data)
      response = { 'data': res }
      self.finish(response)