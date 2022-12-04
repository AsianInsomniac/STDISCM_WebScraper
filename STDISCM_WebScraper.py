import csv
from urllib.request import urlopen
from urllib.request import Request
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time

class webScraper():
    def loadPage(url):
        options = webdriver.ChromeOptions()
        # Option to make browser window visible
        #options.add_argument('--headless')

        # Create a new Chrome session
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(60)
        # Navigate to URL and wait for a few seconds before getting data
        driver.get(url)
        time.sleep(60)

        if driver.page_source != '':
            html = driver.page_source

        driver.quit()
        
        return html

    def getStaffURL(html):
        page_soup = BeautifulSoup(html, "html.parser")
        staffs = page_soup.findAll("button", {"class": "dlsu-pvf-link-button btn btn-link"})
        staffURL = []

        for staff in staffs:
            staffURL.append(staff.get('value'))

        return staffURL

    def getData(url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent,} 

        request = Request(url, None, headers)
        content = urlopen(request).read()
        soup = BeautifulSoup(content, "html.parser")

        # Find email in <a href='mailto:'> link
        for email in soup.find_all('a', attrs={"href": re.compile("^mailto:")}):
            # Get href link
            emailStr = email.get('href')
            # Remove 'mailto:' prefix
            emailStr = emailStr.replace('mailto:', '')
            # Append email to array
            emails.append(emailStr)
            
            # Remove '@dlsu.edu.ph' suffix and remove '.' from staff emails
            emailStr = emailStr.replace('@dlsu.edu.ph', '')
            emailName = emailStr.split('.')

            # Find all <h3> tags (This is where the name per staff page is located)
            for name in soup.find_all('h3'):
                # Case-insensitive substring validation (Check if part of email matches with found name)
                if emailName[0].casefold() in name.text.casefold():
                    # Append name to array
                    names.append(name.text)   

class file():
    def csvOutput(emails, names, url):
        emailCount = 0
        header = ["Email", "Name/Office/Department/Unit"]

        with open("output.csv", "w", newline = '') as csvFile:
            csvWriter = csv.DictWriter(csvFile, fieldnames = header)
            csvWriter.writeheader()
            
            for email, name in zip(emails, names):
                print(email + ' | ' + name)
                csvWriter.writerow({'Email': email, 'Name': name})
                emailCount += 1

        file.txtOutput(url, emailCount)

    def txtOutput(url, emailCount):
        with open("output.txt", "w") as txtFile:
            txtFile.write("URL " + url + "\nNumber of pages scraped: " + "\nNumber of email addresses found: " + str(emailCount))

if __name__=="__main__":
    url = "https://www.dlsu.edu.ph/staff-directory"
    print('URL: ' + url)
    
    while True:
        nTime = input("Scraping Time (minutes): ")

        if(not nTime.isnumeric()):
            print("Only integer inputs are accepted.")
        else:
            if(int(nTime) == 0):
                print("Integer value must be greater than 0.")
            else:
                break

    while True:
        nThread = input("# of Threads/Processes: ")

        if(not nThread.isnumeric()):
            print("Only integer inputs are accepted.")
        else:
            if(int(nThread) == 0):
                print("Integer value must be greater than 0.")
            else:
                break

    start_time = time.time()

    while int((time.time() - start_time) / 60) < int(nTime):
        html = webScraper.loadPage(url)

        if html != '':
            staffURL = webScraper.getStaffURL(html)

            for i in staffURL:
                print(i)

            # Critical Data
            emails = []
            names = []
            nPages = 0
        
            # file.csvOutput(emails, names, url)
        else:
            print("Website timed out.")