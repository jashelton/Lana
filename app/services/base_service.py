from tornado.options import options
from app.services.db import DB

class BaseService(object):
  DB_CONFIG_PATH = "config/db.yml"

  @property
  def db(self):
    if not hasattr(self, '_db'):
      if hasattr(options, 'env'):
        self._db = self._init_db_connection(env=options.env)
      else:
        self._db = self._init_db_connection(env='test')

    return self._db

  def new_session(self):
    return self.db.Session()

  @property
  def tables(self):
    return self.db.tables

  def _init_db_connection(self, env='development'):
    return DB(config_file=self.DB_CONFIG_PATH, env=env)