import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
api_key = os.environ.get("api_key")
endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "ACe7280e1c9053eeba0cd8c18c53a42f86"
auth_token = os.environ.get("auth_token")

# used https://www.latlong.net/ to find my latitude and longitude
weather_params = {
    # Nairobi
    "lat": -1.285790,
    "lon": 36.820030,
    "exclude": "current,minutely,daily",
    "appid": api_key
}
# fetch data from the One Call API
response = requests.get(endpoint, params=weather_params)
response.raise_for_status()
data = response.json()
# link to online jason viewer to view the data http://jsonviewer.stack.hu/
hourly_weather = data["hourly"]
# hourly weather for 12 hours
# get from hour 0 to 11
hours_12 = hourly_weather[:12]

umbrella = False

for hour in hours_12:
    my_weather = hour["weather"]
    weather_id = my_weather[0]["id"]
    if weather_id <= 700:
        umbrella = True
        break

if umbrella:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Lynne, it's gonna rain today 🌧. Don't forget to bring your umbrella🌂!",
        from_='+18454980776',
        # Enter the number here '+1234567890'
        to=''
    )
    print(message.status)

