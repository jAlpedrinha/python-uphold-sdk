
class BaseModel(object):
  def __init__(self, api_client, data):
    self.update_fields(data)
    self.api_client = api_client

  def update_fields(self, data):
    for key, value in data.items():
      setattr(self, key, value)

  def __str__(self):
    return ';'.join(['{}: {}'.format(key, value) for key, value in self.__dict__.items()])

  def __repr__(self):
    return str(self)
