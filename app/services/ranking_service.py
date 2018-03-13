import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class RankingService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  # Return a list of threads for a poll
  def update_poll_rank(self, data):
    update_rank = self._db_session.execute(' \
      update poll_ranking \
      set value = :value, updated_at = curdate() \
      where poll_id = :poll_id and user_id = :user_id; \
    ', dict(value=data['value'], poll_id=data['poll_id'], user_id=data['user_id']))

    new_total_ranking = self.fetch_total_rankings(data['poll_id'])

    self._db_session.commit()
    return dict(message='You have successfully updated your ranking.', data=dict(total_rank=new_total_ranking))
    
  def add_poll_rank(self, data):
    new_rank = self._db_session.execute(' \
      insert into poll_ranking (user_id, value, updated_at, poll_id) values (:user_id, :value, curdate(), :poll_id); \
    ', dict(user_id=data['user_id'], value=data['value'], poll_id=data['poll_id']))

    new_total_ranking = self.fetch_total_rankings(data['poll_id'])

    self._db_session.commit()
    return dict(message='You have successfully ranked a poll.', data=dict(total_rank=new_total_ranking))

  def fetch_total_rankings(self, poll_id):
    total_ranking = self._db_session.execute(' \
      select cast(sum(value) as signed) as total_rank from poll_ranking where poll_id = :poll_id; \
    ', dict(poll_id=poll_id)).fetchone()
    print(total_ranking['total_rank'])
    return total_ranking['total_rank']