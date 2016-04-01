import copy
import json

import aiohttp


class APIClient(object):
  def __init__(self, sandbox = False):
    self.headers = {}
    self.api_url = 'https://api.uphold.com'
    if sandbox:
      self.api_url = 'https://api-sandbox.uphold.com'

  def get_auth_method(self):
    if self.method in ('PAT', 'Basic'):
      return aiohttp.BasicAuth(self.username, self.password)
    return None

  async def get(self, url, data = {}, extra_headers = {}, response = False):
    return await self.api_request('get', url, data, extra_headers, response)

  async def post(self, url, data = {}, extra_headers = {}, response = False):
    return await self.api_request('post', url, data, extra_headers, response)

  async def put(self, url, data = {}, extra_headers = {}, response = False):
    return await self.api_request('put', url, data, extra_headers, response)

  async def delete(self, url, data = {}, extra_headers = {}, response = False):
    return await self.api_request('delete', url, data, extra_headers, response)

  async def patch(self, url, data = {}, extra_headers = {}, response = False):
    return await self.api_request('patch', url, data, extra_headers, response)

  async def api_request(self, method, url, data, extra_headers, return_response):
    async with aiohttp.ClientSession(auth = self.get_auth_method()) as session:
      req_function = getattr(session, method)
      extra_headers.update(self.headers)

      response = await req_function(self.api_url + url, data = data, headers = extra_headers)
      data = await response.json()

      if return_response:
        return data, response

      return data


class WebAppClient(APIClient):
  def __init__(self, token, sandbox = False):
    self.method = 'webapp'
    self.headers['Authorization'] = 'Bearer: {}'.format(self.token)
    super().__init__(sandbox)

  @classmethod
  async def get_access_token(cls, client_id, client_secret, code):
    headers = {
      'Content-Type' : 'application/x-www-form-urlencoded',
      'Accept': 'application/x-www-form-urlencoded',
    }
    payload = {
      'code' : code,
      'grant_type' : 'authorization_code'
    }

    with aiohttp.ClientSession(auth = aiohttp.BasicAuth(client_id, client_secret)) as client:
      response = await client.get(self.api_url + '/oauth2/token', data = json.dumps(payload), headers = headers)

      #Should handle errors here

      data = await response.json()
      return data['access_token']

class PATClient(APIClient):
  def __init__(self, token, sandbox = False):
    self.method='PAT'
    print(token)
    self.username = token
    self.password = 'X-OAuth-Basic'
    super().__init__(sandbox)

  @classmethod
  async def get_access_token(cls, username, password, description, otp = None, sandbox = False):
    payload = { 'description': description }
    headers = { 'Content-Type': 'application/json' }
    api_url = 'https://api.uphold.com'

    if sandbox:
      api_url = 'https://api-sandbox.uphold.com'

    if otp:
      headers['X-Bitreserve-OTP'] = otp

    with aiohttp.ClientSession(auth = aiohttp.BasicAuth(username, password)) as session:
      response = await session.post(api_url + '/v0/me/tokens', data = json.dumps(payload), headers = headers)

      if response.headers.get('X-Bitreserve-OTP', '').lower() == 'required':
        response.close()
        return {"otp": True}

      data = await response.json()
      return data.get('accessToken')
