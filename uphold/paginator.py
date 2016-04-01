import re


class Paginator(object):
  def __init__(self, client, url, limit = None, data = {}, headers = {}, model = None):
    self.offset = 0
    self._count = None
    self.client = client
    self.url = url
    self.limit = limit if limit else 50
    self.data = data
    self.headers = headers
    self.model = model

  def get_model(self):
    return self.model

  def set_model(self, model):
    self.model = model

  async def count(self):
    headers = self.create_range(0,1)
    headers.update(self.headers)

    _, response = await self.client.get(self.url, self.data, headers, response = True)

    if response.status in (412, 416):
      return 0

    content_range = self.parse_content_range(response)
    self._count = content_range['count']

    return self._count

  async def get_next(self):
    next_range = self.get_next_range()

    headers = self.create_range(next_range['start'], next_range['end'])
    headers.update(self.headers)

    data, response = await self.client.get(self.url, self.data, headers, response = True)

    if response.status in (412, 416):
      return 0

    content_range = self.parse_content_range(response)
    self._count = content_range['count']
    self.offset = content_range['last'] + 1

    return [self.model(self.client, item) for item in data]

  async def has_next(self):
    if not self._count:
      await self.count()

    next_range = self.get_next_range()

    if next_range['start'] >= self._count:
      return False

    return True

  def get_next_range(self):
    end = self.offset + self.limit - 1
    if self._count:
      end = min(end, self._count)

    return {
      'end': end,
      'start': self.offset
    }

  def create_range(self, start, end):
    return {
      'Range': 'items={}-{}'.format(start, end)
    }

  def parse_content_range(self, response):
    content_range = response.headers.get('content-range')
    content_range = content_range.split(' ')[-1]
    regex_cr = r'(.*)/(\d*)'
    regex_fp = r'(\d*)-(\d*)'

    first_part, count = re.match(regex_cr, content_range).groups()
    fp_match = re.match(regex_fp, first_part)

    if fp_match:
      offset, last = fp_match.groups()
    else:
      offset, last = 0, 0

    return {
      'offset': int(offset),
      'last': int(last),
      'count': int(count)
    }
