import requests
import os

fcs_api = os.getenv('FCS_API_KEY')

class Fcs():
    def get_important_forex_news(self) -> str:
            url = 'https://fcsapi.com/api-v3/forex/economy_cal'
            params = {
                'access_key': fcs_api
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an exception if the response status is not OK (2xx)

                json_data = response.json()
                important_events = []
                for item in json_data['response']:
                    if item['importance'] == '2':
                        important_events.append(item)
                return important_events

            except requests.exceptions.RequestException as e:
                
                return f'Error fetching data from FCS API:{e}'