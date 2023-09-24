# to pull my favorites in from Hacker News and index tokenize them
from bs4 import BeautifulSoup
import requests
import time

with open('links4.txt','w') as f:
    for i in range(1,25):
        time.sleep(1)
        html_doc = requests.get('https://news.ycombinator.com/favorites?id=bgilroy26&p=' + str(i))
        soup = BeautifulSoup(html_doc.text, 'html.parser')

        for tag in soup.find_all('a'):
            if tag['href']:
                if 'item' in tag['href']:
                    if 'comments' in tag.text:
                        if int(tag.text[:tag.text.find('c')-1]) < 50:
                            f.write('https://news.ycombinator.com/' + \
                                    tag.get('href') + '\n')
                        else:    
                            title_line = tag.find_previous('span', {'class':'titleline'})
                            title_link = title_line.a['href']
                            f.write(title_link)
                            f.write('\n')
