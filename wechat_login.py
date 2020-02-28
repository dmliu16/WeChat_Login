import requests
import json
from PIL import Image

import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import numpy as np

from dateutil import tz
from datetime import datetime
from datetime import timedelta 

from collections import Counter
from sae_log_util import SaeLogFetcher

# 1) get access token
# 2) post to get QR ticket
# 3) get ticket url

# 1)

appid = 'wx58e39f4b2b2856ef'
appsecret = 'cd06220b05f530262f626124a8739c71'
url0 = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+appsecret

r0 = requests.get(url0).content

# convert to string
token_string = r0.decode()

# convert to dictionary
token_dict = json.loads(token_string)

# get access token from the dictionary
access_token = token_dict["access_token"]


# 2)

post_json = '{"expire_seconds": 60, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}'
url1 = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token='+access_token

r1 = requests.post(url1, data = post_json).content

# convert to string to dictionary
ticket_string = r1.decode()
ticket_dict = json.loads(ticket_string)

ticket = ticket_dict["ticket"]


# 3)

url2 = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='+ticket
r2 = requests.get(url2).content

with open("qr.png", "wb") as img:
    img.write(r2)

# get time right now
def getChinaTime():
	# UTC Zone
	from_zone = tz.gettz('UTC')
	# China Zone
	to_zone = tz.gettz('Asia/Shanghai')
	utc = datetime.utcnow()
	# Tell the datetime object that it's in UTC time zone
	utc = utc.replace(tzinfo=from_zone)

	# Convert time zone
	local = utc.astimezone(to_zone)

	china_date = datetime.strftime(local, "%Y-%m-%d")
	china_time = datetime.strftime(local, "%d/%b/%Y %H:%M:%S")


	return [datetime.strptime(china_time, "%d/%b/%Y %H:%M:%S"), china_date]

# get openid and time
def getOpenId_time():
	date = getChinaTime()[1]
	service = 'http'
	ident = 'access'
	fop = '' 
	version = 1

	ACCESSKEY = '3y44mkxx1x'
	SECRETKEY = '4ikiliykhw2mhlyxxk213wk0m41kwyh5mlilh4z1'

	log_fetcher = SaeLogFetcher(ACCESSKEY, SECRETKEY)

	result = log_fetcher.fetch_log(service, date, ident, fop, version)
	try:
		result = result.decode('latin-1') 

		content = result.split('\n')[:-1]

		info = ''

		for i in range(len(content)-1, -1, -1):
			if ("POST" in content[i] and "openid" in content[i]):
				info = content[i]
				break

		# Extract the openid
		# this parse the string and get the openid
		openid = info[info.find("openid"):].split()[0][7:]
		time = info[(info.find("[")+1):info.find(" +")]

		date_time = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
		return [openid, date_time]
	except:
		print("No data in this date: " + date)
		return ['', datetime.utcnow()-timedelta(hours=12)]

	


scanTime = getChinaTime()[0]

qr_code = Image.open('qr.png')
qr_code.show()

# get time of qr code show
time_show = datetime.utcnow()
time_end = datetime.utcnow() + timedelta(seconds=60)

openid = ''

# compare time and see if time is after scanTime
while datetime.utcnow() <= time_end:
	openid_time = getOpenId_time()

	if scanTime < openid_time[1]:
		openid = openid_time[0]
		break

class Open_ID:
	def __init__(self):
		self.id = openid

	def getID(self):
		return self.id

url3 = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"
r3 = requests.get(url3)

import json

user_info = json.loads(r3.content.decode())


from tkinter import *

from PIL import Image
import requests
from io import BytesIO
from PIL import ImageTk,Image

master = Tk()

canvas_width = 760
canvas_height = 400
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

url = user_info['headimgurl']
response = requests.get(url)

head = Image.open(BytesIO(response.content)).resize((280, 280), Image.ANTIALIAS)
headshot = ImageTk.PhotoImage(head)  

#w.create_line(0, y, canvas_width, y, fill="#476042")
w.create_image(60, 60, anchor=NW, image=headshot)  
w.create_text(3*canvas_width / 4 , 3*canvas_height / 12, text="昵称：" + user_info['nickname'])
w.create_text(3*canvas_width / 4 , 5*canvas_height / 12, text="地区：" + user_info['country'] + " " + user_info['province']
	+ " " + user_info['city'])

sex = ""
if user_info['sex'] == 1: 
	sex = "男"
elif user_info['sex'] == 2:
	sex = "女"
else:
	sex = " "

w.create_text(3*canvas_width / 4, 7*canvas_height / 12, text="性别：" + sex)


mainloop()



