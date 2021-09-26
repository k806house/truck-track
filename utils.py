import requests

from envs import API_KEY

def get_coords_by_address(address):
    payload = {
        'address': address,
        'key': API_KEY,
    }

    try:
        r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json', params=payload)
        response = r.json()
        if response["status"] != "OK":
            print(response)
            print(f'Failed request:\naddress {address}')
            return (None, None)
        location = response["results"][0]["geometry"]["location"]
    except:
        print(response)
        print(f'Failed request:\naddress {address}')
        return (None, None)
    return (location["lat"], location["lng"])

def dest(src_lat, src_lon, dest_lat, dest_lon):
    payload = {
        'origin': f'{src_lat},{src_lon}',
        'destination': f'{dest_lat},{dest_lon}',
        'key': API_KEY,
    }

    try:
        r = requests.get(f'https://maps.googleapis.com/maps/api/directions/json', params=payload)
        response = r.json()
        if response["status"] != "OK":
            print(response)
            print(f'Failed request:\norigin {src_lat},{src_lon}\ndestination {dest_lat},{dest_lon}')
            return
        distance = response["routes"][0]["legs"][0]["distance"]["value"]
        distance /= 1000
    except:
        print(response)
        print(f'Failed request:\norigin {src_lat},{src_lon}\ndestination {dest_lat},{dest_lon}')
        return
    return distance