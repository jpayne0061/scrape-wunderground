import requests
from bs4 import BeautifulSoup
import re

url = "https://www.wunderground.com/history/airport/KSDF/2017/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=2017&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="

source_code = requests.get(url)
soup = BeautifulSoup(source_code.text)

master_table = soup.find('div', {'id': 'observations_details'})
rows = master_table.findAll('tr')


all_records = []

month = 0
day = 0

for row in rows:
    #skip if it has headers
    
    if(len(row.findAll('th')) > 0):
        continue
    
    first_col_text = row.findAll('td')[0].text
    
    if(first_col_text.isdigit()):
        
        day = int(first_col_text)
        tds = row.findAll('td')
        
        high = re.sub('[^0-9]','', tds[1].text)
        
        events = tds[-1].text.replace("\t", "").replace("\n", "").replace("\xa0", "").replace(",", " ")
        
        date = '2017-' + str(month) + '-' + str(day)
        
        data = {'date': date, 'high' : high, 'events': events}
        
        all_records.append(data)
    else:
        month += 1
        

def add_zeros_to_single_nums(num_string):
    if(len(num_string) == 1):
        return '0' + num_string
    else:
        return num_string

#add our header
with open("ville-weather.csv", 'a') as f:
	     f.write("date,high,events" + "\n")
    
for record in all_records:
    with open("ville-weather.csv", 'a') as f:
        date = record['date'].split('-')
        record['date'] = date[0] +'-'+add_zeros_to_single_nums(date[1])+'-'+add_zeros_to_single_nums(date[2])
        line = record['date'] + ',' + record['high'] + ',' + record['events']
        f.write(line + "\n")


        
    
    
    
    
    
    
    
    
