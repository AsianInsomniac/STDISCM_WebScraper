import csv
import multiprocessing
import queue
import pandas as pd
import re
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

nPages = 0

class webScraper(object):
    def timer(event, nTime):
        print("Timer started.", flush=True)
        time.sleep(nTime * 60.0)
        event.set()
        print("Timer ended.", flush=True)

    def producer(url, q, nTime):
        html = webScraper.getData(url, nTime)
        
        if html != '':
            # Prefixes to be removed from the URL
            prefixes = ['https://www.dlsu.edu.ph', 'http://www.dlsu.edu.ph']
            # Excluded links (Invalid, Duplicate with minor syntax difference, or leads outside of the DLSU domain)
            exclude = ['#', 'javascript:;', 'javascript:void(0)', '/', 'www.dlsu.edu.ph', '/about-dlsu', '/colleges', '/students/international',
                       'https://www.facebook.com/DLSU.Manila.100', 'https://twitter.com/dlsumanila', 'https://www.linkedin.com/school/de-la-salle-university/',
                       'https://www.youtube.com/channel/UC7LXC9usdkDC0YEvWxa_kHQ', 'https://twitter.com/DLSUGradStudies', 'https://www.facebook.com/DLSU.GradStudies']
            print("Getting all URLs.", flush=True)

            page_soup = BeautifulSoup(html, "html.parser")
            page_body = page_soup.find('body')
            urlListRaw = page_body.find_all('a', href=True)
            urlList = []

            for url in urlListRaw:
                if all(url.get('href') != x for x in exclude):
                    urlRaw = url.get('href')

                    for prefix in prefixes:
                        if(prefix in urlRaw):
                            urlRaw = urlRaw.replace(prefix, '')

                    urlList.append(urlRaw)

            urlList = pd.unique(urlList)

            for url in urlList:
                q.put(url)

            print("Finished getting URLs.", flush=True)
        else:
            print("No URLs loaded.")

    def consumer(q, nTime, event, emails):
        print("Waiting to get URL from queue.", flush=True)

        while not event.is_set():
            try:
                qURL = q.get(True, nTime * 60.0)
            except TimeoutException:
                print("Timeout.", flush=True)
            except queue.Empty:
                print("Queue is empty.", flush=True)
            except None:
                print("No data retrieved.")
            else:
                print("Process is now getting data from " + qURL, flush=True)

                qLink = ''

                if(qURL < 'https:'):
                    qLink = 'https://www.dlsu.edu.ph'

                qLink = qLink + qURL
                html = webScraper.getData(qLink, nTime)
                webScraper.getEmail(html, emails)

                print('Successfully parsed data from ' + qURL, flush=True)
        print("Event is set.", flush=True)

    def getData(url, nTime):
        html = ''
        options = webdriver.ChromeOptions()
        # Option to make browser window invisible
        options.add_argument('--headless')
        # Create a new Chrome session
        driver = webdriver.Chrome(options=options)
        # Navigate to URL and wait for the page to fully load before getting data
        print(f"Loading {url}.", flush=True)

        try:
            driver.get(url)  
            WebDriverWait(driver=driver, timeout=nTime * 60.0).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        except TimeoutException:
            print("Website timed out.", flush=True)
        except:
            print("An unknown error has occurred when loading the website.", flush=True)
        else:
            print("Website loaded.", flush=True)
            html = driver.page_source
        finally:
            driver.quit()

        return html

    def getEmail(html, emails):
        if html != '':
            page_soup = BeautifulSoup(html, "html.parser")
            page_body = page_soup.find('body')
            emailRaw = page_body.find_all('a', attrs={"href": re.compile("^mailto:")})
            
            for email in emailRaw:
                emailStr = email.get('href')
                emailStr = emailStr.replace('mailto:', '')
                emails.append(emailStr)
                print(emailStr, flush=True)

            global nPages
            nPages = nPages + 1

class file():
    def csvOutput(emails):
        header = ["Email"]

        with open("output.csv", "w", newline = '') as csvFile:
            csvWriter = csv.DictWriter(csvFile, fieldnames = header)
            csvWriter.writeheader()
            
            for email in emails:
                print(email)
                csvWriter.writerow({'Email': email})

    def txtOutput(url, nPages, emailCount):
        with open("output.txt", "w") as txtFile:
            txtFile.write("URL: " + url + "\nNumber of pages scraped: " + str(nPages) + "\nNumber of email addresses found: " + str(emailCount))

if __name__ == "__main__":
    url = "https://www.dlsu.edu.ph"

    while True:
        urlInput = input("URL (https): ")

        if(url not in urlInput):
            print("Only websites under the DLSU domain can be used.")
        else:
            break
    
    while True:
        nTime = float(input("Scraping Time (minutes): "))

        if(nTime <= 0.0):
            print("Scraping time must be greater than 0.")
        else:
            break

    while True:
        nProcess = input("# of Processes: ")

        if(not nProcess.isnumeric()):
            print("Only integer inputs are accepted.")
        else:
            if(int(nProcess) == 0):
                print("Integer value must be greater than 0.")
            else:
                break

    q = multiprocessing.Queue()
    event = multiprocessing.Event()
    processes = []
    emails = []

    pProc = multiprocessing.Process(target=webScraper.producer, name='Producer', args=(urlInput, q, nTime, ))
    pProc.start()
    
    for i in range(int(nProcess)):
        processes.append(multiprocessing.Process(target=webScraper.consumer, name='Consumer ' + str(i), args=(q, nTime, event, emails, )))
        processes[i].start()    

    pProc.join()

    webScraper.timer(event, nTime)    

    for process in processes:
        print("Joining process.", flush=True)
        process.join()
        if process.is_alive():
            print("Terminating process.", flush=True)
            process.terminate()
        print(process.name + ' ended.')

    file.csvOutput(emails)
    file.txtOutput(urlInput, nPages, len(emails))
    print("output.csv and output.txt generated.", flush=True)

    sys.exit()