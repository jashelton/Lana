from app.handlers.base_handler import BaseHandler
from app.services.question_service import QuestionService
from app.helpers.auth_helper import jwtauth
from app.models.errors import HTTPError

@jwtauth
class QuestionHandler(BaseHandler):
  def get(self, the_id=None, **kwargs):
    current_user = self.get_arguments("user_id")
    if the_id:
      # questions/:id
      # TODO: CHECK IF USER HAS ALREADY TAKEN POLL
      res = QuestionService().one(the_id, int(current_user[0]))
      response = {'data': res}
      self.finish(response)
    else:
      # /questions
      res = QuestionService().all(int(current_user[0]))
      response = { 'data': res }
      self.finish(response)
