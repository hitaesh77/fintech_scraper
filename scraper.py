import requests
import pandas as pd
from bs4 import BeautifulSoup

# initialize scraper by reading file and creating a dictionary
def initialize_scraper():
    # Read the Excel file containing company names and URLs
    urls_df = pd.read_excel("urls.xlsx")
    companies = urls_df.loc[:, "Names"].tolist()
    urls = urls_df.loc[:, "Links"].tolist()
    
    # Initialize an empty dictionary to store job links
    intern_dict = {}
    for company in companies:
        print(company)
        intern_dict[company] = []
    
    return urls, intern_dict

# TODO: Implement the function to search for student jobs
def search_student_jobs(url, intern_dict):
    # Placeholder function for searching student jobs
    # This function can be expanded to scrape job postings from the given URL
    pass

# Read URLs from the file
def load_dict(urls, intern_dict):
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

if __name__ == "__main__":
    urls, intern_dict = initialize_scraper()
    
    load_dict(urls, intern_dict)
    
    print("Scraping completed.")