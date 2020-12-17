import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_url(position, location):
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url


def get_record(card):
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://www.indeed.com' + atag.get('href')
    company = card.find('span', 'company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div', 'summary').text.strip().replace("\n", " ")
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime("%Y-%m-%d")
    try:
        job_salary = card.find('span', 'salaryText').text.strip()
    except:
        job_salary = ""
    
    record = (job_title, company, job_location, post_date, today, job_summary, job_salary, job_url)
    
    return record

    
    
        

def main(position, location):
    records = []
    url = get_url(position, location)
    
    
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all("div", "jobsearch-SerpJobCard")
        
        for card in cards:
            records.append(get_record(card))
        
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except:
            break

    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Post Date', 'Extract Date', 'Summary', 'Salary', 'Job Url'])
        writer.writerows(records)
        
        
search_job = input("Enter job: ")
search_location = input("Enter location: ")
main(search_job, search_location)