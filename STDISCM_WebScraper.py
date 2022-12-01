import csv

class webScraper():
    pass

class file():
    def csvOutput():
        header = ["Email", "Name", "Office", "Department/Unit"]

        with open("output.csv", "w") as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(header)

        pass

    def txtOutput(url):
        with open("output.txt", "w") as txtFile:
            txtFile.write("URL: " + url + "\nNumber of pages scraped: " + "\nNumber of email addresses found: ")

if __name__=="__main__":
    url = "https://www.dlsu.edu.ph"

    while True:
        urlInput = input("URL: ")

        if(urlInput != url):
            print("Only the DLSU website can be used for this project.\n")
        else:
            break
    
    nTime = input("Scraping Time (minutes): ")
    
    # OPTIONAL: Number of threads/processes to be used
    nThread = input("# of Threads/Processes to be used: ")

    file.txtOutput(url)
    file.csvOutput()