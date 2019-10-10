import requests
import json
key = ''
token = ''
OAuth = ''
board_id = ''


members = []

def get_members():

	url = "https://api.trello.com/1/boards/{}/members".format(board_id)
	querystring = {"key":key,"token":token}
	response = requests.request("GET", url, params=querystring)
	res_text = response.text 
	res = json.loads(res_text)
	for r in res:
		mem = {}
		mem['id'] = r['id']
		mem['username'] = r['username']
		mem['fullName'] = r['fullName']
		mem['score'] = 0
		members.append(mem)

def get_list_done_id():
	url = "https://api.trello.com/1/boards/{}/lists".format(board_id)
	querystring = {"cards":"none","card_fields":"all","filter":"open","fields":"all","key":key,"token":token}
	response = requests.request("GET", url, params=querystring)
	res_text = response.text
	res = json.loads(res_text)
	for r in res:
		if r['name'] == 'Done':
			return r['id']
	return ''


def add_score():
	done_id = get_list_done_id()
	url = 'https://api.trello.com/1/lists/{}/cards?filds=all'.format(done_id)
	querystring = {"key":key,"token":token}
	response = requests.request("GET", url, params=querystring)
	# print(response.text)
	res_text = response.text
	res = json.loads(res_text)
	for r in res:
		for i in r['idMembers']:
			for m in members:
				if i == m['id']:
					s = 0
					for l in r['labels']:
						print(l)
						if l['name'].find('điểm') != -1:
							s += int(l['name'][:1])
					m['score'] += s
	members_text = json.dumps(members)
	print(members_text)

if __name__ == '__main__':
	get_members()
	add_score()
	file_name = board_id + '.json'
	with open(file_name, 'w') as file:
		json.dump(members,file)


