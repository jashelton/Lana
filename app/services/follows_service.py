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