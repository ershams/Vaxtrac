from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


page = requests.get('https://www.drugs.com/drug-class/vaccine-combinations.html')

bSoup = BeautifulSoup(page.content, 'html.parser')
table = bSoup.find('table')
thead = table.find('thead')
column_names = [th.text.strip() for th in thead.find_all('th')]

data = []
for row in table.find_all('tr'):
    row_data = []
    for td in row.find_all('td'):
        td_check = td.find('a')
        if td_check is not None:
            link = td.a['href']
            row_data.append(link)
        else:
            not_link = ''.join(td.stripped_strings)
            if not_link == '':
                 not_link = None
            row_data.append(not_link)
    data.append(row_data)
df = pd.DataFrame(data[1:], columns=column_names)
df_dict = df.to_dict('records')

# for row in df_dict:
#     print(row)

links = []


for i in range(len(df_dict) -1):
    links.append(df_dict[i]['Drug Name'])
# print(links)


linkslist = []
for i in links:
    
    # linkslist.append(url)
    linkslist.append(f"https://www.drugs.com{i}")
# print(linkslist)

for i in linkslist:
    page1 = requests.get(i)
    priorix = BeautifulSoup(page1.content, 'html.parser')

    target = priorix.find('h2')
    print(target.parent)
    texts = target.find_next_sibling('p')

    # print(dir(texts))
    print(texts.children)
    # for text in texts:
    #     print(text)

# for i  in linkslist:
#     page2 = requests.get(i)
#     priorix1 = BeautifulSoup(page2.content, 'html.parser')
#     target1 = priorix1.find('h2', text='Before taking this medicine')
#     texts1 = target1.find_next('p')
#     # for text1 in texts1:
    #     print(text1)

