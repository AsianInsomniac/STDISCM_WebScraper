import csv
from datetime import datetime
from dataclasses import dataclass
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import pandas as pd

class webScraper():
    def getData(url):
        # Arrays for Data
        @dataclass
        class webEntry:
            email: str
            name: str
        
        entries = []

        emails = []
        names = []

        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # driver.get(url)
        # content = driver.page_source
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent,} 

        request = Request(url, None, headers)
        content = urlopen(request).read()
        soup = BeautifulSoup(content, "html.parser")
        
        for email in soup.find_all('a', attrs={"class": "btn btn-sm btn-block text-capitalize"}):
            emailStr = email.get('href')
            emailStr = emailStr.replace('mailto:', '')
            emails.append(emailStr)
        for name in soup.find_all('h3'):
            names.append(name.text)

        file.csvOutput(emails, names, url)

class file():
    def csvOutput(emails, names, url):
        emailCount = 0
        header = ["Email", "Name/Office/Department/Unit"]

        with open("output.csv", "w", newline = '') as csvFile:
            csvWriter = csv.DictWriter(csvFile, fieldnames = header)
            csvWriter.writeheader()
            
            for email, name in zip(emails, names):
                print(email + ' | ' + name)
                csvWriter.writerow({'Email': email, 'Name/Office/Department/Unit': name})
                emailCount += 1

        file.txtOutput(url, emailCount)

    def txtOutput(url, emailCount):
        with open("output.txt", "w") as txtFile:
            txtFile.write("URL " + url + "\nNumber of pages scraped: " + "\nNumber of email addresses found: " + str(emailCount))

if __name__=="__main__":
    url = "https://www.dlsu.edu.ph"

    while True:
        urlInput = input("URL (https): ")

        if(url not in urlInput):
            print("Only the DLSU website can be used for this project.")
        else:
            break
    
    while True:
        nTime = input("Scraping Time (minutes): ")

        if(not nTime.isnumeric()):
            print("Only integer inputs are accepted.")
        else:
            break
    
    # OPTIONAL: Number of threads/processes to be used
    while True:
        nThread = input("# of Threads/Processes to be used: ")

        if(not nThread.isnumeric()):
            print("Only integer inputs are accepted.")
        else:
            break

    webScraper.getData(urlInput)