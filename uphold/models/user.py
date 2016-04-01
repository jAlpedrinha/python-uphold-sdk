from uphold.paginator import Paginator
from .base import BaseModel
from .card import Card
from .transaction import Transaction

class User(BaseModel):
  async def get_updated_data(self):
    data = await self.api_client.get('/v0/me')
    self.update_fields(data)

  async def get_balances(self):
    await self.get_updated_data()
    return self.balances['currencies']

  async def get_balance_by_currency(self, currency):
    await self.get_updated_data()
    if not currency in self.balances['currencies']:
      return {'error' : 'no such currency'}
    return self.balances['currencies'][currency]

  async def get_card_by_address(self, address):
    return await self.get_card_by_id(address)

  async def get_card_by_id(self, ID):
    data = await self.api_client.get('/v0/me/cards/{}'.format(ID))
    return Card(self.api_client, data)

  async def get_cards(self):
    data = await self.api_client.get('/v0/me/cards')
    return [Card(self.api_client, item) for item in data]

  async def get_cards_by_currency(self, currency):
    data = await self.api_client.get('/v0/me/cards')
    cards = [Card(self.api_client, card) for card in data if card['currency'] == currency]
    return cards

  async def get_contacts(self):
    data = await self.api_client.get('/v0/me/contacts')
    return [Contact(self.api_client, contact) for contact in data]

  def get_country(self):
    return self.country

  def get_currencies(self):
    return self.currencies

  def get_email(self):
    return self.email

  def get_first_name(self):
    return self.first_name

  def get_last_name(self):
    return self.last_name

  def get_name(self):
    return self.name

  async def get_phones(self):
    return await self.api_client.get('/v0/me/phones')

  async def get_settings(self):
    await self.get_updated_data()
    return self.settings

  def get_state(self):
    return self.state

  def get_status(self):
    return self.status

  async def get_total_balance(self):
    await self.get_updated_data()
    return {
      'amount' : self.balances['total'],
      'currency': self.settings['currency']
    }

  def get_transactions(self, limit = None):
    return Paginator(self.api_client, '/v0/me/transactions', limit = limit, model = Transaction)

  def get_username(self):
    return self.username

  def create_card(self, label, currency):
    return Card.create(self.api_client, label, currency)

  async def update(self, data):
    data = await self.api_client.patch('/v0/me/', data = data)
    self.update_fields(data)

  async def revoke_token(self, token = None):
    if not token and not self.api_client.method == 'PAT':
      return {'error': 'No PAT defined'}
    if not token:
      token = self.api_client.username

    _, response = await self.api_client.delete('/v0/me/tokens/{}'.format(token), response = True)
    status = response.status

    if status != 204:
      return False

    return True
