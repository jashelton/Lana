import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class FollowsService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def all(self, user):
    # +----------------------------------------------------------+
    # |  |
    # +----------------------------------------------------------+

    pass

  def follow_user(self, user_to_follow, data):
    self._db_session.execute(' \
      insert into follows(user_id, follower_id, followed_date, unfollowed_date) \
        values(:user_to_follow, :current_user, curdate(), null) \
    ', dict(user_to_follow=user_to_follow, current_user=data['current_user']))
    self._db_session.commit()

    return 'Successfully followed'

  def unfollow_user(self, user_to_unfollow, data):
    self._db_session.execute(' \
      delete from follows where user_id = :user_to_unfollow and follower_id = :current_user' \
    , dict(user_to_unfollow=user_to_unfollow, current_user=data['current_user']))
    self._db_session.commit()

    return 'Successfully unfollowed'