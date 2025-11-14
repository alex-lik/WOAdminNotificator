import requests
from config import TG


tg = TG()


def send_message(message):
	try:
		url = f"https://api.telegram.org/bot{tg.token}/sendMessage"
		params = { "chat_id": tg.chat_id, "text": message, }
		resp = requests.get(url, params=params)
		# resp.raise_for_status()
		return resp
	except:pass

def pin_message(msg_id):
	url = f"https://api.telegram.org/bot{tg.token}/pinChatMessage"
	params = { "chat_id": tg.chat_id, "message_id": msg_id }
	resp = requests.get(url, params=params)
	resp.raise_for_status()
	return resp


def unpin_message(msg_id):
	try:
		url = f"https://api.telegram.org/bot{tg.token}/unpinChatMessage"
		params = {"chat_id": tg.chat_id, 'message_id': msg_id }
		resp = requests.get(url, params=params)
		# resp.raise_for_status()
		return resp
	except: 
		pass

def edit_message(msg_id, message):
	try:
		url = f"https://api.telegram.org/bot{tg.token}/editMessageText"
		params = { "chat_id": tg.chat_id, "message_id": msg_id, "text": message }
		resp = requests.get(url, params=params)
		# resp.raise_for_status()
		return resp
	except: pass