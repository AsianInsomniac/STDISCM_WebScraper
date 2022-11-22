# STDISCM Parallel Programming Project: Email Address Web Scraper

---

## Description

<p>An organization uses websites to disseminate information to potential customers or partners about the
organization. An organization’s website normally posts email addresses as contact information.
Scraping email addresses each page manually in a website takes a long time. A web scraper is an
automated tool that can scrape pages in the website. The web scraped can be programmed to
automatically find email addresses using parallel programming techniques.</p>

---

## Project Requirements

- [] Create a Python email web scraper program that finds email addresses from the [DLSU Website](https://www.dlsu.edu.ph) in a specific amount of time
	- [] Input Arguments (GUI/Command Line)
		- URL
		- Scraping Time (in minutes)
		- <em>Optional:</em> Number of threads/processes to be used
	- [] Output Files
		- [] .CSV file that contains the following:
			- [] Email
			- [] Name
			- [] Office
			- [] Department or unit
		- [] .TXT file that contains statistics of the website:
			- [] URL
			- [] Number of pages scraped
			- [] Number of email addresses found
			
---

## Documentation - [Template](https://www.ieee.org/conferences/publishing/templates.html)

<ol>
	<li>[] Introduction</li>
		- Brief discussion/summary of the program and its requirement
	<li>[] Program Implementation</li>
		- Discussion on how the program was implemented
			- Use of locks or semaphores
			- Sharing of data between processes
			- Parallel programming and optimization techniques used
	<li>[] Result</li>
		- Discussion of the results and explanation/analysis on why it was achieved
	<li>[] Conclusion</li>
		- How was parallel programming used in this project?
		- How did parallel programming improve/worsen/neutrally affect performance?
	<li>[] References</li>
</ol>