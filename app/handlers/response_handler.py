from app.handlers.base_handler import BaseHandler
from app.services.response_service import ResponseService

class ResponseHandler(BaseHandler):
  ITEMS = ('response', 'create')
  def get(self, item=None, **kwargs):
    if item == 'response':
      print('get response')

  def post(self, item, **kwargs):
    self.load_json()

    if item == 'response':
      poll_response = self.request.arguments
      res = ResponseService().create_response(poll_response['data'])
      response = { 'data': res }
      self.finish(response)

    elif item == 'create':
      poll_data = self.request.arguments
      res = ResponseService().create_poll(poll_data['poll'])
      response = { 'data': res }
      self.finish(response)
