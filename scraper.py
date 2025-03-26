import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pywhatkit as kit

key_locations = ["chicago", "new york", "boston", "los angeles", "san francisco", "seattle", "austin", "philadelphia", "remote"]
phone_number = "+haha you thought"

# helper functions:
def is_valid_url(url):
    parsed = urlparse(url)
    # A valid URL must have a scheme (e.g., "http") and a netloc (e.g., "example.com")
    return bool(parsed.scheme) and bool(parsed.netloc)

# Function to print the intern dictionary for easier testing and debugging
def print_intern_dict(intern_dict):
    for company, jobs in intern_dict.items():
        print(f"{company}:", ", ".join(jobs) if jobs else "No student jobs found.")

# Function to test individual comapanies: helps validate job class and location classes
def test_company(company, intern_dict):
    if company in intern_dict:
        print(f"{company}:", ", ".join(intern_dict[company]) if intern_dict[company] else "No student jobs found.")
    else:
        print(f"{company} not found in the dictionary.")

# whatsapp message test
def send_message(message):
    kit.sendwhatmsg_instantly(phone_number, message, 10, tab_close=True)

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
    #job_titles = [job.text.strip() for job in job_elements]
    #return job_titles
    job_titles = []
    for job in job_elements:
        # Extract all text inside the parent element (including nested tags)
        cleaned_text = " ".join(job.stripped_strings)  # Handles deeply nested text
        if cleaned_text:
            job_titles.append(cleaned_text)

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
    #print_intern_dict(intern_dict)
    test_company("Susquehanna", intern_dict)
    
    print("Scraping completed.")

    #testing
    send_message("What's up gang") 