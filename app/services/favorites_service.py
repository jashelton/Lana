import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class FavoritesService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def add_favorite(self, user, poll):
    sql = (' \
      insert into favorites(timestamp, user_id, poll_id) values(curdate(), :user_id, :poll_id); \
    ')

    self._db_session.execute(sql, dict(user_id=user, poll_id=poll))
    self._db_session.commit()
    return 'Successfully added to favorites.'

  def delete_favorite(self, user, poll):
    sql = (' \
      delete from favorites where poll_id = :poll_id and user_id = :user_id; \
    ')

    self._db_session.execute(sql, dict(poll_id=poll, user_id=user))
    self._db_session.commit()

    return 'Successfully removed from favorites.'