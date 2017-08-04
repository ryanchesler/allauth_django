import requests

gamers = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=575D6F2C240C96CB1ADB5122D6675BF2&steamids='[u'76561198246842444']'")
gamers = gamers.json()
print gamers