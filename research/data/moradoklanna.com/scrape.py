from bs4 import BeautifulSoup
import requests
from pythainlp.util import collate
import urllib.parse

sortDict = []
moradoklannaDict = []
words = []

alphabets = ["ก", "ข", "ฃ", "ค", "ฅ", "ฆ", "ง", "จ", "ฉ", "ช", "ซ", "ฌ", "ญ", "ฎ", "ฏ", "ฐ", "ฑ", "ฒ", "ณ", "ด", "ต", "ถ", "ท", "ธ", "น", "บ", "ป", "ผ", "ฝ", "พ", "ฟ", "ภ", "ม", "ย", "ร", "ล", "ว", "ศ", "ษ", "ส", "ห", "ฬ", "อ", "ฮ"]
vowels = ["ะ", "ั", "า", "ิ", "ี", "ึ", "ื", "ุ", "ู", "เ", "แ", "ไ", "ใ", "โ", "ใ", "ำ"]

for alphabet1 in alphabets:
    for alphabet2 in alphabets:
        words.append(f"{alphabet1}{alphabet2}")

for alphabet in alphabets:
    for vowel in vowels:
        words.append(f"{alphabet}{vowel}")


def getInfo(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
 
    if not table:
        print(f"No table in {url}")
        return
    # Loop through each row in the table
    for row in table.find_all('tr'):
        # Check if the row should be excluded based on bgcolor
        if row.get('bgcolor') == '#aaaaaa':
            continue
        
        # Get all the cells in the row
        cells = row.find_all('td')

        haveWord = False

        for wordInfo in moradoklannaDict:
            if wordInfo['word'] != cells[0].text.strip():
                continue
            else:
                haveWord = True

        if haveWord == False:
            moradoklannaDict.append({
                'word': cells[0].text.strip(),
                'lanna': cells[1].text.strip(),
                'pronounciation': cells[2].text.strip(),
                'definition': cells[3].text.strip().replace('\"','\\"'),
                'source': 'moradoklanna.com'
            })
            
            sortDict.append(cells[0].text.strip())
 
for word in words:
    getInfo(f'https://moradoklanna.com/dict/?s={word}')


output_file = "C:/Users/maewa/Programming/Thai-NorthernTh/Data/moradoklanna.com/moradoklannaDict.json"

with open(output_file, 'w', encoding='utf-8') as f:

        Dict = collate(sortDict)
        Id = 1
        f.write('[\n')
        for i in range(len(Dict)):
            for j in range(len(moradoklannaDict)):
                if Dict[i] == moradoklannaDict[j]['word']:

                    moradoklannaDict[j]['thTran'] = ""
                    moradoklannaDict[j]['id'] = Id 

                    if Id == 1:
                        f.write(' {\n')
                    else:
                        f.write(',\n {\n')

                    for key, value in moradoklannaDict[j].items():
                        if key == "id":
                            f.write('  "%s":"%s"\n' % (key, value))
                        else:
                            f.write('  "%s":"%s",\n' % (key, value))
                    
                    f.write(' }')

                    moradoklannaDict.pop(j) #กันเจอคำต้นซ้ำ
                    Id += 1
                    break

        f.write('\n]')