import requests
import re
text = requests.get('https://store.steampowered.com/hardware/steamcontroller').text
print(re.findall(r'window\.[\w_]+\s*=', text)[:10])
print(re.findall(r'data-store-[\w_]+', text)[:10])
print(re.findall(r'\"steam_controller.*?', text)[:10])
