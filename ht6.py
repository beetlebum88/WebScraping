import requests
from bs4 import BeautifulSoup
import json

url = "https://www.bbc.com/sport"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

data = []

promo_wrappers = soup.find_all('div', {'class': 'ssrcss-1va2pun-UncontainedPromoWrapper eqfxz1e5'})

count = 0

for promo_wrapper in promo_wrappers:
    promo_link = promo_wrapper.find('a', {'class': 'ssrcss-vdnb7q-PromoLink exn3ah91'})
    if promo_link:
        link = "https://www.bbc.com" + promo_link['href']

        metadata_text = promo_wrapper.find('span', {'class': 'ssrcss-1if1g9v-MetadataText e4wm5bw1'})
        if metadata_text:
            topic = metadata_text.text.strip()

            data.append({
                "Link": link,
                "Topics": [topic]
            })

            count += 1

            if count == 5:
                break

if count == 0:
    print("No promo wrappers found on the page.")
else:

    with open('bbc_json.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f"JSON file 'bbc_sport_promos.json' created successfully with {count} entries.")
