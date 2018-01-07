from tornado.options import options
from app.services.db import DB
from sqlalchemy import select
from datetime import datetime, timedelta
import re
import os
import jwt
# from app.models.single_use_token import SingleUseToken
from app.models.errors import UserNotFoundError
from app.models.errors import InvalidTokenError, InvalidParametersError
import bcrypt

class Auth(object):
  """Class to handle login/logout"""
  def __init__(self, email=None, password=None):
    self.email = email
    self.password = password
    self.user = None
    self.env = options.env
    self._db = DB(config_file='config/db.yml', env=self.env)
    self.db_session = self._db.Session()

  def login(self):
    user_table = self._db.tables['users']
    self.user = self.get_user(self.db_session, user_table)
    # todo: add user to users table
    return self.user and self.verify_password(user_table)

  def get_user(self, db_session, user_table):
    user_id = db_session.execute(select([user_table.c.id]).where(user_table.c.username == self.email)).fetchone()
    if user_id:
      return user_id[0]
    else:
      raise UserNotFoundError(reason="User not found")

  def verify_password(self, user_table):
    hashed_pw = self.db_session.execute(select([user_table.c.password])
                                        .where(user_table.c.id == self.user)).fetchone()[0]
    return bcrypt.checkpw(self.password.encode(encoding='UTF-8', errors='strict'),
                          hashed_pw.encode(encoding='UTF-8', errors='strict'))

  # def record_login(self, *, ip=None):
  #   L = self._db.tables['logins']
  #   login = {'ip': ip, 'user_id': self.user, 'created_at': datetime.now(), 'updated_at': datetime.now()}
  #   res = self.db_session.execute(L.insert().values(login))
  #   self.db_session.commit()
  #   return res.inserted_primary_key[0]

