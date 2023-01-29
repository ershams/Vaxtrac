# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import json

# def get_vacc_ed(url):

#     page = requests.get(url)

#     combVac = BeautifulSoup(page.content, 'html.parser')
#     table = combVac.find('table')
#     thead = table.find('thead')
#     column_names = [th.text.strip() for th in thead.find_all('th')]

#     data = []
#     for row in table.find_all('tr'):
#         row_data = []
#         for td in row.find_all('td'):
#             td_check = td.find('a')
#             if td_check is not None:
#                 link = td.a['href']
#                 row_data.append(link)
#             else:
#                 not_link = ''.join(td.stripped_strings)
#                 if not_link == '':
#                     not_link = None
#                 row_data.append(not_link)
#         data.append(row_data)
#     df = pd.DataFrame(data[1:], columns=column_names)
#     df_dict = df.to_dict('records')
#     # print(df_dict)

#     return df_dict
# # for row in df_dict:
# #     print(row)

# viral_list = []
# combo_list = []
# bact_list = []
# viral_list = get_vacc_ed('https://www.drugs.com/drug-class/viral-vaccines.html')
# combo_list = get_vacc_ed('https://www.drugs.com/drug-class/vaccine-combinations.html')
# bact_list = get_vacc_ed('https://www.drugs.com/drug-class/bacterial-vaccines.html')

# LINKS = []

# def add_links_to_list(list):
#     for i in range(len(list) -1):
#         LINKS.append(list[i]['Drug Name'])

# add_links_to_list(viral_list)
# add_links_to_list(combo_list)
# add_links_to_list(bact_list)

# # print(LINKS)
# editedlinks = []

# for i in LINKS:
#     editedlinks.append(i[1:-5])

# print(editedlinks)


# linkslist = []
# for i in LINKS:
    
#     linkslist.append(f"https://www.drugs.com{i}")
# # print(len(linkslist))

# for i in linkslist:
#     page1 = requests.get(i)
#     education = BeautifulSoup(page1.content, 'html.parser')

#     target = education.find('h2')
#     texts = target.find_next_sibling('p').text
#     # print(texts)
    

# # for i  in linkslist:
# #     page2 = requests.get(i)
# #     priorix1 = BeautifulSoup(page2.content, 'html.parser')
# #     target1 = priorix1.find('h2', text='Before taking this medicine')
# #     texts1 = target1.find_next('p')
# #     # for text1 in texts1:
#     #     print(text1)
