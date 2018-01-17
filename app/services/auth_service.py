import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
import bcrypt
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class AuthService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()
  
  def register(self, user_info):
    password = bcrypt.hashpw(user_info['password'].encode(encoding='UTF-8', errors='strict'), bcrypt.gensalt())

    sql = text(' \
      insert into users(name, username, password, created_at) values(:name, :username, :password, curdate()) \
    ')

    self._db_session.execute(sql, dict(name=user_info['name'], username=user_info['username'], password=password))
    self._db_session.commit()

    return 'Successfully registered'
