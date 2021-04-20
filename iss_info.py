import requests
import json
import datetime
from geocode import get_coordinates, get_location


ADDRESS = 'Karol Bagh'


def get_data(lat, lon):
	"""
	Gets the relevant data using coord from the iss api and converts it to a dict
	"""
	
	coord = (lat, lon)

	URL1 = 'http://api.open-notify.org/iss-now.json'
	r = requests.get(URL1)
	positional_data = json.loads(r.text)

	URL2 = 'http://api.open-notify.org/iss-pass.json'
	payload = {'lat': float(coord[0]), 'lon': float(coord[1])}
	r = requests.get(URL2, params=payload)
	passes_data = json.loads(r.text)

	URL3 = 'http://api.open-notify.org/astros.json'
	r = requests.get(URL3)
	crew_data = json.loads(r.text)

	return positional_data, passes_data, crew_data


def display_data(): 
	positional_data, passes_data, crew_data = get_data(*get_coordinates(ADDRESS))

	long_now = float(positional_data['iss_position']['longitude'])
	# long_now = str(abs(long_now)) + ' Degrees {}'.format('East' if long_now > 0 else 'West')
	lat_now = float(positional_data['iss_position']['latitude'])
	# lat_now = str(abs(lat_now)) + ' Degrees {}'.format('North' if lat_now > 0 else 'South')

	passes = [
		(response['duration'], 
			datetime.datetime.fromtimestamp(response['risetime']).strftime('%d %b %H:%M:%S'))\
		for response in passes_data['response']
	]

	print(f'\nThe ISS is currently at - \n{get_location(lat_now, long_now)}\n')

	print(f"At the coordinates ( {passes_data['request']['latitude']}, {passes_data['request']['longitude']} ) , The ISS will pass over {passes_data['request']['passes']} times. -")
	for pass_ in passes:
	    print(f'On {pass_[1]} for a duration of {pass_[0]} seconds')

	print(f"\nCurrently {crew_data['number']} people are on the ISS - ")
	for person in crew_data['people']:
	    print(person['name'])


if __name__ == '__main__':
	display_data()

    