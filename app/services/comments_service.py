import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class CommentsService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  # Return a list of threads for a poll
  def get_threads_by_poll(self, poll_id):
    # +--------------------------------------------------+
    # | id | text | created_at | username | num_comments |
    # +--------------------------------------------------+
    sql_threads = self._db_session.execute(' \
      select T.id, T.text, T.created_at, U.username, count(C.id) as num_comments from threads T \
      left join comments C on C.thread_id = T.id \
      join users U on U.id = T.user_id \
      where T.poll_id = :poll_id \
      group by T.id, T.text, T.created_at, U.username; \
    ', dict(poll_id=poll_id)).fetchall()

    return [dict(zip(row.keys(), row)) for row in sql_threads]

  # Return a nested list of comments by thread
  def get_comments_by_thread(self, thread_id):
    # +-------------------------------------------------------------------------+
    # | id | thread_id | parent_id | user_id | created_at | text | has_children |
    # +-------------------------------------------------------------------------+
    sql_comments = self._db_session.execute(' \
      select C1.*, U.username, \
      exists (select 1 from comments C2 where C2.thread_id = C1.thread_id and C2.parent_id = C1.id) as has_children \
      from comments C1 \
      join users U on U.id = C1.user_id \
      where C1.thread_id = :thread_id; \
    ', dict(thread_id=thread_id)).fetchall()
    comments = [dict(zip(row.keys(), row)) for row in sql_comments]

    roots = [comment for comment in comments if comment['parent_id'] is None]
    for root in roots:
      if root['has_children']:
        root['comments'] = self.get_children(root, comments)
    return roots

  def get_children(self, parent, comments):
    child_comments = [c for c in comments if c['parent_id'] == parent['id']]
    for comment in child_comments:
      if comment['has_children']:
        comment['comments'] = self.get_children(comment, comments)
    return child_comments

  def add_thread(self, data):
    sql_create_thread = text(' \
      insert into threads(poll_id, text, created_at, user_id) values(:poll_id, :text, curdate(), :user_id); \
    ')

    self._db_session.execute(sql_create_thread, dict(
      poll_id=data['poll_id'],
      text=data['text'],
      user_id=data['user_id']))

    last_thread_id = self._db_session.execute('SELECT LAST_INSERT_ID();').fetchone()[0]

    thread_response = self._db_session.execute(' \
      select T.id, T.text, T.created_at, U.username, count(C.id) as num_comments from threads T \
      left join comments C on C.thread_id = T.id \
      join users U on U.id = T.user_id \
      where T.id = :thread_id \
      group by T.id, T.text, T.created_at, U.username; \
    ', dict(thread_id=last_thread_id)).fetchall()

    thread = [dict(zip(row.keys(), row)) for row in thread_response]

    self._db_session.commit()
    return dict(message='You have successfully created a thread.', thread=thread[0])

  def add_comment(self, data):
    sql_create_comment = text(' \
      insert into comments(thread_id, parent_id, user_id, created_at, text) values(:thread_id, :parent_id, :user_id, curdate(), :text); \
    ')

    self._db_session.execute(sql_create_comment, dict(
      thread_id=data['thread_id'],
      parent_id=data['parent_id'],
      user_id=data['user_id'],
      text=data['text']))

    last_comment_id = self._db_session.execute('SELECT LAST_INSERT_ID();').fetchone()[0]

    comment_response = self._db_session.execute(' \
      select C.*, U.username \
      from comments C \
      join users U on U.id = C.user_id \
      where C.id = :comment_id; \
    ', dict(comment_id=last_comment_id)).fetchall()

    comment = [dict(zip(row.keys(), row)) for row in comment_response]

    self._db_session.commit()
    return dict(message='You have successfully added a comment.', comment=comment)