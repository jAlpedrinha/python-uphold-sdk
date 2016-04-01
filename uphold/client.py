import asyncio
import json

import aiohttp

from uphold import models
from uphold.api_client import WebAppClient, PATClient, APIClient

class UpholdClient(object):
  def __init__(self, sandbox = False, client_id = None, client_secret = None):
    self.api_url = 'https://api.uphold.com/'
    self.client_id = client_id
    self.client_secret = client_secret
    self.api_client = APIClient(sandbox = sandbox)
    self.sandbox = sandbox

    if self.sandbox:
      self.api_url = 'https://api-sandbox.uphold.com/'

  async def authorize_user(self, code):
    #We shhould handle errors here
    token = await WebAppClient.get_access_token(self.client_id, self.client_secret, code)
    self.api_client = WebAppClient(token, sandbox = self.sandbox)
    return True

  async def create_token(self, username, password, description = 'Python sdk', otp = None):
    result = await PATClient.get_access_token(username, password, description, otp, sandbox = self.sandbox)
    if isinstance(result, dict):
      return result
    self.api_client = PATClient(result, sandbox = self.sandbox)
    return True

  async def get_user(self):
    data = await self.api_client.get('/v0/me')
    print(data)
    return models.User(self.api_client, data)
