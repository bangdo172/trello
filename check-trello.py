import requests
import json
key = 'd068e39d5caa008d15f6f24bde23d11b'
token = 'fad342244c0c1a57ede7bd8f00b8a60c7b3c61c705dd40b3d985140e0d3512e0'
OAuth = 'aef8bca5d65464ade50fd6907e229bcf5dd7a590865a625c35ede7d96e9dd9c3'
board_id = '5EZXKSVg'

# id_board = '5c92654753d5420546584c20'

# id_list_done = '5c92656207d35f360e119493'

# id_card_test = '5d6a161b710a8b7d9c9af458'

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


