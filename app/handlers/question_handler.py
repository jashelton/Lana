from app.handlers.base_handler import BaseHandler
from app.services.question_service import QuestionService
from app.models.errors import HTTPError

class QuestionHandler(BaseHandler):
  ITEMS = ('questions')
  def get(self, the_id=None, **kwargs):
    print(the_id)
    print(**kwargs)
    if the_id:
      print('--found id--')
      print(the_id)
      # questions/:id
      res = QuestionService().one(the_id)
      response = {'data': res}
      print(response)
      self.finish(response)
    else:
      # /questions
      res = QuestionService().all()
      response = { 'data': res }
      print(response)
      self.finish(response)
