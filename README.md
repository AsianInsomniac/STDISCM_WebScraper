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

- [X] Create a Python email web scraper program that finds email addresses from the [DLSU Website](https://www.dlsu.edu.ph) in a specific amount of time
	- [X] Input Arguments (GUI/Command Line)
		- URL
		- Scraping Time (in minutes)
		- <em>Optional:</em> Number of threads/processes to be used
	- [X] Output Files
		- [X] .CSV file that contains the following:
			- [X] Email
			- [X] Name
		- [X] .TXT file that contains statistics of the website:
			- [X] URL
			- [X] Number of pages scraped
			- [X] Number of email addresses found
			
---

## Documentation - [Template](https://www.ieee.org/conferences/publishing/templates.html)

<ol>
	<li>[X] Introduction</li>
		- Brief discussion/summary of the program and its requirement
	<li>[X] Program Implementation</li>
		- Discussion on how the program was implemented
			- Use of locks or semaphores
			- Sharing of data between processes
			- Parallel programming and optimization techniques used
	<li>[X] Result</li>
		- Discussion of the results and explanation/analysis on why it was achieved
	<li>[X] Conclusion</li>
		- How was parallel programming used in this project?
		- How did parallel programming improve/worsen/neutrally affect performance?
	<li>[X] References</li>
</ol>