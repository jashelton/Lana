import yaml
from sqlalchemy import create_engine, MetaData, orm

class DB(object):
  def __init__(self, *, config_file, env='development'):
    self._env = str(env or 'development')
    with open(config_file, 'r') as yamlfile:
      self._cfg = yaml.safe_load(yamlfile).get(self._env)
      if not self._cfg:
        raise RuntimeError('Missing environment "{0}" in db config "{1}".'.format(self._env, config_file))
      self._meta = MetaData()
      engine = create_engine(self.connection_string)
      self._meta.reflect(bind=engine)
      self._sessionClass = orm.sessionmaker(bind=engine)

  @property
  def Session(self):
    return self._sessionClass

  @property
  def connection_string(self):
    return '{db_engine}://{username}:{password}@{host}/{database}'.format_map(self._cfg)

  @property
  def env(self):
    return self._env

  @property
  def tables(self):
    return self._meta.tables

  def __str__(self):
    return repr(self)

  def __repr__(self):
    return "{0}(env={1}, conn={2})".format(type(self).__name__, self._env, self.connection_string)