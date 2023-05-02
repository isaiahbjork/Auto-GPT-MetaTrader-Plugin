import requests
import os

lunarcrush_api = os.getenv('LUNAR_CRUSH_API_KEY')

class LunarCrush():
    def get_stock_of_the_day(self) -> float:
        url = "https://lunarcrush.com/api3/stockoftheday"
        headers = {
            'Authorization': f'Bearer {lunarcrush_api}'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return response.text.encode('utf8')
        else:
            raise Exception(
                f"Failed to get Stock of the day from LunarCrush; status code {response.status_code}")
