import requests
import re

text = requests.get('https://store.steampowered.com/search/results?term=Steam+Controller').text
matches = re.findall(r'href="https://store.steampowered.com/app/(\d+)/[^\"]*"[^>]*>.*?<span class="title">Steam Controller</span>', text, re.DOTALL)
print('App IDs:', matches)

matches2 = re.findall(r'href="https://store.steampowered.com/app/(\d+)/[^\"]*"[^>]*>.*?<span class="title">Steam Controller \(2015\)</span>', text, re.DOTALL)
print('App IDs 2015:', matches2)

# Steam Deck
matches3 = re.findall(r'href="https://store.steampowered.com/app/(\d+)/[^\"]*"[^>]*>.*?<span class="title">Steam Deck', text, re.DOTALL)
print('Steam Deck:', matches3)
