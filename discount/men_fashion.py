import os
import requests
from bs4 import BeautifulSoup

path = 'F:\discounts\discount\static\img'
os.chdir(path)  
    
url = 'https://www.amazon.com/s?k=men+fashion&crid=3L77H40KI6CSS&sprefix=iphone%2Caps%2C453&ref=nb_sb_noss_1'

headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
images = soup.find_all('img', {'class':'s-image'})
for image in images:
    name = image['alt']
    link = image['src']
    print(name, link)
    
    # with open(name+'.jpg', 'wb') as f:
    #     im = requests.get(link)
    #     f.write(im.content)