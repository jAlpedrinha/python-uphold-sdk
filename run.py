import asyncio

from prompt_toolkit import prompt

from uphold import UpholdClient

async def test(username, password):
  sdk = UpholdClient(sandbox = True)
  result = await sdk.create_PAT(username, password)
  print(result)
  if result.get('otp'):
    otp = prompt("Insert OTP:")
    result = await sdk.create_PAT(username, password, otp = otp)

  sdk.addPAT(result.get('accessToken'))
  data = await sdk.get_cards()
  print(data)

if __name__ == '__main__':
  sdk = UpholdClient(sandbox = True)
  username = 'XXXXXXXXXXX'
  password = 'XXXXXXXXX'
  loop = asyncio.get_event_loop()
  loop.run_until_complete(test(username,password))
