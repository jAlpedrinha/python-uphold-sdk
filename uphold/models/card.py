from .base import BaseModel


class Card(BaseModel):
  @classmethod
  async def create(cls, api_client, label, currency):
    data = api_client.post('/v0/me/cards', data = {'label': label, 'currency': currency})
    return cls(api_client, data)
