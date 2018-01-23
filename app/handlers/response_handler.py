from app.handlers.base_handler import BaseHandler
from app.services.response_service import ResponseService

class ResponseHandler(BaseHandler):
  ITEMS = ('response', 'create')
  def get(self, item=None, **kwargs):
    if item == 'response':
      print('get response')
    elif item == 'create':
      print('create')

  def post(self, item, **kwargs):
    self.load_json()

    if item == 'response':
      poll_response = self.request.arguments

      res = ResponseService().create_response(poll_response['data'])
      response = { 'data': res }
      self.finish(response)