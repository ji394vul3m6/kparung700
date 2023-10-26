import requests
from bs4 import BeautifulSoup

def getInfo(session, date):
  url = "http://www.kparung700.com/camp/campOrder.php?date={}&campying_id=#info".format(date)
  response = session.get(url)
  content = response.content.decode('utf-8')

  body = BeautifulSoup(content, 'html.parser')
  attrs = {
    "name": "tpl"
  }
  tplInput = body.find('input', attrs)
  available = body.find('div', {'class': 'camp_lists'}).find('section').find_all('li')
  return tplInput.attrs['value'], available

def addArea(session, id, useno, d, order_day_num):
  url='http://www.kparung700.com/order/campy_num_ajax.php?act=show_data&campying_id='+id+'&num=1&store_useno='+useno+'&date='+d+'&order_day_num='+order_day_num
  response = session.get(url)
  content = response.content.decode('utf-8')
  print("id: {}, result: {}".format(id, content))

def order(date, maxNum = 8):
  s = requests.Session()
  tpl, availables = getInfo(s, date)
  ok = 0
  availables.reverse()
  for available in availables:
    onchange = [x.strip("')") for x in available.find('select').attrs['onchange'].split(',')]
    id = onchange[1]
    useno = onchange[2]
    d = onchange[3]
    order_day_num= onchange[7]
    addArea(s, id, useno, d, order_day_num)
    ok += 1
    if ok >= maxNum:
      break

  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  request_body = {
    "tpl": tpl,
    "order_date": date,
    "name": "姓名", # required
    "phone": "0900000123", # required
    "mail": "email@example.com", # required
    "ps": "",
    "agree": "on"
  }
  response = s.post("http://www.kparung700.com/camp/pro_edit.php", request_body, headers)
  content = response.content.decode('utf-8')
  print(content)

order('2023-12-18', 2)