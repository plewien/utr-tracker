import logging as log
import requests


class Session:
	def __init__(self, url):
		self.session = requests.Session()
		self.url = url

	def safe_get(self, uri):
		with self.session.get(self.url + uri) as response:
			if (not response.ok):
				raise response.raise_for_status()
			return response.json()

	def safe_post(self, url, uri, headers=None, body=None):
		with self.session.post(url + uri, headers=headers, json=body) as response:
			if (not response.ok):
				raise response.raise_for_status()
			return response.json()


class UTRSession(Session):
	api_version='v1'
	def __init__(self):
		super().__init__('https://api.universaltennis.com')
		self.app_url = 'https://app.universaltennis.com/api'

	def login(self, username, password):
		uri = f'/{self.api_version}/auth/login'
		headers = {'Content-Type': 'application/json'}
		body = {'email' : username, 'password' : password}
		self.safe_post(self.app_url, uri, headers, body)
		log.debug(f'Successful login for {username}')
		return self

	def find_id(self, name):
		query = f'query={name}'
		data = self.safe_get(f'/{self.api_version}/search/players?top=1&{query}')
		if data['total'] == 0:
			raise Exception(f'Unable to find player ID for {name}: Zero results')
		elif data['total'] > 1:
			log.warning(f"{data['total']} players found with the same name")

		return data['hits'][0]['id']

	def get_profile_data(self, id):
		data = self.safe_get(f'/v1/player/{id}/profile')
		log.debug(f'Profile data: {data}')
		return data

	def get_player_data(self, id, name=None):
		if not id and not name:
			raise Exception("Must specify either a player name or id")
		elif not id:
			id = self.find_id(name)

		log.info(f"Searching stats for id {id}...")
		data = self.safe_get(f'/{self.api_version}/player/{id}/profile')

		log.info("Player found: {} with UTR {}/{} in {} {}, {}".format( \
				data['displayName'], data['singlesUtr'], data['doublesUtr'], \
				data['location']['cityName'], data['location']['stateAbbr'], data['location']['countryName']))
		return data
