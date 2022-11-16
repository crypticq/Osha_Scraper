from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import pandas as pd


data = []
url = "https://www.oshatrain.org/pages/professional-training-courses.html"

driver = webdriver.Firefox()
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'lxml')



course = soup.find_all('div', {'class': 'courseFeaturesList'})


def strip_text(text):
    return float((text.split(" ")[0]).strip())


for x in range(len(course)):
    try:
        if x > 80:
            title = soup.findAll('a')[x].text
            if "View Course Page" in title:
                continue
            Modules = (course[x].find_all('li')[0].text)
            hours = (course[x].find_all('li')[1].text)
            h = float((hours.split(" ")[0]).strip())

            data.append(
                {
                    'title': title,
                    'Modules': strip_text(Modules),
                    'hours': strip_text(hours),
                    "course": (f"https://www.oshatrain.org{soup.findAll('a')[x]['href'].split('.')[-2]}.html")

                }
            )



    except Exception as e:
        print(e)
        pass




driver.close()

print('Working for data frame')
df = pd.DataFrame(data)
print(df)
df.to_excel('osha.xlsx', index=True)
