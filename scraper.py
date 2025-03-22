import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# helper functions:
def is_valid_url(url):
    parsed = urlparse(url)
    # A valid URL must have a scheme (e.g., "http") and a netloc (e.g., "example.com")
    return bool(parsed.scheme) and bool(parsed.netloc)
    # return bool(parsed.netloc)

def get_full_url(base_url, relative_url):
    if(is_valid_url(relative_url)):
        return relative_url
    elif relative_url.startswith("//"):
        relative_url = "https:" + relative_url
        return relative_url
    elif relative_url.startswith("/"):
        return base_url + relative_url

def normalize_job_links(base_url, job_links):
    for i, link in enumerate(job_links):
        job_links[i] = get_full_url(base_url, link)



# initialize scraper by reading file and creating a dictionary
def initialize_scraper():
    # Read the Excel file containing company names and URLs
    urls_df = pd.read_excel("urls.xlsx")
    companies = urls_df.loc[:, "names"].tolist()
    career_urls = urls_df.loc[:, "careers"].tolist()
    base_urls = urls_df.loc[:, "base"].tolist()
    job_classes = urls_df.loc[:, "job_classes"].tolist()
    location_classes = urls_df.loc[:, "location_classes"].tolist()
    
    # Initialize an empty dictionary to store job links
    intern_dict = {}
    for company in companies:
        print(company)
        intern_dict[company] = []
    
    return companies, career_urls, base_urls, job_classes, location_classes, intern_dict

# Function to search for student jobs in the job titles and add them to the dictionary
def search_student_jobs(job_titles, company, intern_dict):
    for title in job_titles:
        if "intern" in title.lower() or "student" in title.lower() or "summer" in title.lower():
            intern_dict[company].append(title)

# Function to scrape job titles from a given career URL
def get_job_titles(career_url, job_class_name):
    response = requests.get(career_url)
    html_data = response.text
    soup = BeautifulSoup(html_data, 'html.parser')
    job_elements = soup.find_all(class_=job_class_name)  
    job_titles = [job.text.strip() for job in job_elements]
    return job_titles

# Initial loading of the intern dictionary
def load_dict(career_urls, job_classes, companies, intern_dict):
    for i, career_url in enumerate(career_urls):
        career_url = career_url.strip() # removes whitespace
        if not career_url:
            continue  # Skip empty lines
        
        job_titles = get_job_titles(career_url, job_classes[i])
        search_student_jobs(job_titles, companies[i], intern_dict)

if __name__ == "__main__":
    companies, career_urls, base_urls, job_classes, location_classes, intern_dict = initialize_scraper()
    
    load_dict(career_urls, job_classes, companies, intern_dict)
    print(intern_dict)
    
    print("Scraping completed.")