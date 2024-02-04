import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
# business-categories


#to getRespone from a website
def getResponse(url):
    try:
        response = requests.get(url)
        if response.status_code ==200:
         return response.text
    except Exception as e:
        print(e)
    
#To Extract list of categories from Google my business
def listOfCategories(text):
    try:
     soup = BeautifulSoup(text,'html.parser')
     ul = soup.find('ul',class_="business-categories")
     categories = [ i.text for i in ul.find_all('li')]
     return categories
    except Exception as e:
       print(e)

#To scrape details from Google maps
def dataScraping(categories):
    try:
        driver = webdriver.Chrome()
        driver.get(f"https://www.google.com/maps/search/{categories}+in+Andhra+Pradesh/")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.find_all('div', class_="UaQhfb fontBodyMedium")
        data =[]
        for div in divs:
            name_element = div.find('div', class_='qBF1Pd fontHeadlineSmall')
            address_element = div.find_all('div',class_="W4Efsd")[2]
            contact_element = div.find('span', class_='UsdlK')
            name = name_element.text.strip() if name_element else " "
            address = address_element.text.strip() if address_element else " "
            contact_details = contact_element.text.strip() if contact_element else " "
            data.append({
               'category':categories,
                'Name': name,
                'Address': address,
                'Contact Details': contact_details
            })
        return data
    except Exception as e:
        print(e)
    finally:
        driver.quit()


# Converting the extracted data from google maps to Excel format
def toExcel(categories):
    try:
        companydata =pd.DataFrame()
        for i in categories[0:100]:
            data= dataScraping(i)
            df = pd.DataFrame(data)
            companydata=pd.concat([companydata,df],ignore_index=True)
        companydata.to_excel('DigipplusAssignment.xlsx')
    except Exception as e:
        print(e)


#calling function 
txt = getResponse("https://daltonluka.com/blog/google-my-business-categories")
categories = listOfCategories(txt)
toExcel(categories)