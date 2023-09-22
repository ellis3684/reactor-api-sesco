"""
The reactor unit names in 'powerreactorstatusforlast365days.txt' do not match the unit names provided in other
documents that contain information about each reactor.

I did find this web page 'https://www.nrc.gov/reactors/operating/project-managers.html' which contains unit names that
match those provided in 'powerreactorstatusforlast365days.txt'.

Since this page contains a docket number for each reactor, I scraped the docket number for each reactor. The docket
number can then be used to match each reactor in 'powerreactorstatusforlast365days.txt' with a reactor in
'reactors-operating.xlsx', wherein individual reactor data can be obtained.
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


url = 'https://www.nrc.gov/reactors/operating/project-managers.html'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')

reactor_trs = soup.find('table').find_all('tr')[1:]  # Skip header row
reactors_and_dockets = {}
for tr in reactor_trs:
    anchor_tag = tr.find('a')
    docket_td = tr.find_all('td')[1]
    reactor_name = anchor_tag.string
    docket_num = docket_td.string

    # This is the only name on the web page that is inconsistent with the name in 'powerreactorstatusforlast365days.txt'
    if reactor_name == 'River Bend 1':
        reactors_and_dockets['River Bend Station 1'] = docket_num
    else:
        reactors_and_dockets[reactor_name] = docket_num

pd.DataFrame(reactors_and_dockets.items(), columns=['Unit', 'DocketNum']).to_csv('units_and_dockets.csv')


def get_docket_num(row):
    unit = row.Unit
    if unit == 'Vogtle 4':  # 'Vogtle 4' is not on the web page, nor is it in 'reactors-operating.xlsx'
        return
    return reactors_and_dockets[unit]


status_df = pd.read_csv('external/powerreactorstatusforlast365days.txt', sep='|')
status_df['DocketNum'] = status_df.apply(get_docket_num, axis=1)
status_df.to_csv('status_w_dockets.csv')
