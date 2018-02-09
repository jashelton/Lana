from app.handlers.base_handler import BaseHandler
from app.services.favorites_service import FavoritesService
from app.models.errors import HTTPError

class FavoritesHandler(BaseHandler):
  def post(self, **kwargs):
    # /favorites
    self.load_json()
    data = self.request.arguments
    poll_id = data['poll']['id']
    user_id = data['user_id']

    res = FavoritesService().add_favorite(user_id, poll_id)
    response = { 'data': res }
    self.finish(response)

  def delete(self, **kwargs):
    self.load_json()
    data = self.request.arguments

    res = FavoritesService().delete_favorite(data['user_id'], data['poll_id'])
    response = { 'data': res }
    self.finish(response)