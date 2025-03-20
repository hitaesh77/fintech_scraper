import requests
from bs4 import BeautifulSoup

urls = open("urls.txt", "r")
intern_dict = {}

# Read URLs from the file
for url in urls:
    url = url.strip()
    if not url:
        continue  # Skip empty lines

    job_links = []
    response = requests.get(url)
    html_data = response.text
    soup = BeautifulSoup(html_data, 'html.parser')
    all_links = soup.find_all(name="a")
    for link in all_links:
        href = link["href"]
        if "job" in href.lower() or "jobs" in href.lower():
            job_links.append(href)
    
    print("Filtered Job Links:")
    for job in job_links:
        print(job)

urls.close()