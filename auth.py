import asyncio
from prompt_toolkit import prompt

from uphold.api_client import PATClient
from uphold import UpholdClient

async def test(username, password):
  client = UpholdClient(sandbox = False)

  token = await client.create_token(username, password, "Testing")

  if isinstance(token, dict):
    otp = prompt('Insert OTP:')
    success = await client.create_token(username, password, "Testing", otp = otp)

  user = await client.get_user()

  # btc_balance = await user.get_balance_by_currency('BTC')
  # print('BTC balance: ', btc_balance)
  #
  # btc_cards = await user.get_cards_by_currency('BTC')
  # print('BTC cards: ', btc_cards)
  #
  # btc_card_by_id = await user.get_card_by_address('mh7hnZ41MJy69BP1ApYg2Hp8iEzvAKzbmB')
  # print('BTC card by id ', btc_card_by_id)
  #
  # contacts = await user.get_contacts()
  # print('Contacts ', contacts)
  #
  # phones = await user.get_phones()
  # print('Phones', phones)
  #
  # settings = await user.get_settings()
  # print('Settings', settings)
  #
  # total_balance = await user.get_total_balance()
  # print('Total Balance: ', total_balance)

  transactions_pager = user.get_transactions()
  # has_next = await transactions_pager.has_next()
  # print('Has more transactions? ', has_next)
  #
  # if has_next:
  transactions = await transactions_pager.get_next()
  print('Transactions', transactions)


  answer = await user.revoke_token()
  print('Revoking token', answer)

if __name__ == '__main__':
  username = 'XXXXX'
  password = 'XXXXXXx'
  loop = asyncio.get_event_loop()
  loop.run_until_complete(test(username,password))
