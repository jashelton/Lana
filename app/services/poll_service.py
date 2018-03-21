import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class PollService(BaseService):
  # TODO: A lot of stuff in question service/handler should be moved to poll service/handler
  def __init__(self):
    self._db_session = self.new_session()

  def get_poll_by_user(self, user, current_user):
    # +-----------------------------------------------+
    # | poll_id | created_at | question_id | question |
    # +-----------------------------------------------+
    sql_username = text(' \
      select id from users where username = :user; \
    ')

    username = self._db_session.execute(sql_username, dict(user=user)).fetchone()

    sql_polls_by_action = text(' \
      select PE.id, PE.poll_id as poll_id, PE.action, PE.timestamp as created_at, Q.id as question_id, Q.question, U.username \
      from poll_events PE \
      join questions Q on PE.poll_id = Q.poll_id \
      join users U on U.id = PE.user_id \
      where PE.user_id = :user_id and Q.type = "primary"; \
    ')

    polls_activity = self._db_session.execute(sql_polls_by_action, dict(user_id=username['id'])).fetchall()

    social = self._db_session.execute(' \
      select count(F1.id) as following, \
      (select count(F2.id) from follows F2 where follower_id = :user_id) as followers, \
      exists (select 1 from follows F3 where F3.follower_id = :current_user ) as is_following \
      from follows F1 where user_id = :user_id; \
    ', dict(user_id=username['id'], current_user=current_user)).fetchone()

    # social = self._db_session.execute(' \
    #   select * from follows where user_id = :user_id or follower_id = :user_id;', \
    #   dict(user_id=username['id'])).fetchall()

    data = dict(
      activity = [dict(zip(row.keys(), row)) for row in polls_activity],
      social=dict(
        following=social['following'],
        followers=social['followers'],
        is_following=social['is_following']
      )
    )
    print(data)

    return data
