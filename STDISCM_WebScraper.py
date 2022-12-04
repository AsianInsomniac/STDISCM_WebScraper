import csv
from urllib.error import HTTPError
import requests
import re
import time
import multiprocessing
from urllib.request import urlopen
from urllib.request import Request
from selenium import webdriver
from bs4 import BeautifulSoup

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
        time.sleep(30)

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

    def getData(emails, names, url, nPages):
        print(f"Accessing staffURL[{nPages}]")
        s.acquire()

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent,} 

        request = Request(url, None, headers)

        try:
            content = urlopen(request).read()
            soup = BeautifulSoup(content, "html.parser")
        except HTTPError:
            print(f"HTTP Timeout occurred on staffURL[{nPages}].")

        # Find email in <a href='mailto:'> link
        for email in soup.find_all('a', attrs={"href": re.compile("^mailto:")}):
            # Get href link
            emailStr = email.get('href')
            # Remove 'mailto:' prefix
            emailStr = emailStr.replace('mailto:', '')
            # Append email to array
            emails.append(emailStr)
            print(emailStr)
            
            # Remove '@dlsu.edu.ph' suffix and remove '.' from staff emails
            emailStr = emailStr.replace('@dlsu.edu.ph', '')
            emailName = emailStr.split('.')

            # Find all <h3> tags (This is where the name per staff page is located)
            for name in soup.find_all('h3'):
                # Case-insensitive substring validation (Check if part of email matches with found name)
                if emailName[0].casefold() in name.text.casefold():
                    # Append name to array
                    names.append(name.text)
                    print(name.text)
        
        nPages += 1

        s.release()
        print(f"Done with staffURL {nPages}")

class file():
    def csvOutput(emails, names, url):
        emailCount = 0
        header = ["Email", "Name"]

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

    s = multiprocessing.Semaphore(int(nThread))

    html = webScraper.loadPage(url)
    if html != '':
        staffURL = webScraper.getStaffURL(html)

        for i in staffURL:
                print(i)

        start_time = time.time()
        while (((time.time() - start_time) / 60.0) < (float(nTime) * 60.0)):
            threads = []
            
            # Critical Data
            emails = []
            names = []
            nPages = 0

            for i in range(len(staffURL)):
                threads.append(multiprocessing.Process(target = webScraper.getData(emails, names, 'https://www.dlsu.edu.ph/staff-directory?personnel=' + staffURL[nPages], nPages)))
                threads[i].start()

            for i in range(len(staffURL)):
                threads[i].join()
        
        file.csvOutput(emails, names, url)   

        end_time = time.time()
        print(int((end_time - start_time) / 60))
    else:
        print("Website timed out.")
        
    
    