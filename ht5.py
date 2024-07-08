import requests
import re
import json
import sqlite3


def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"There is no information: {response.status_code}"
    except requests.RequestException as e:
        return f"Error: {e}"


def extract_job_titles(html_content):
    pattern = re.compile(r'<h3 class="jobCard_title">(.*?)</h3>', re.IGNORECASE)
    job_titles = pattern.findall(html_content)
    return job_titles


def extract_job_links(html_content):
    pattern = re.compile(r'<a href="(https://www\.lejobadequat\.com/emplois/.*?)"', re.IGNORECASE)
    job_links = pattern.findall(html_content)
    return job_links


def save_to_json(data, filename='jobs.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_sqlite(data, db_name='jobs.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT
        )
    ''')
    for job in data:
        c.execute('INSERT INTO jobs (title, url) VALUES (?, ?)', (job['title'], job['url']))
    conn.commit()
    conn.close()


url = "https://www.lejobadequat.com/emplois"
page_content = get_page_content(url)

if isinstance(page_content, str):
    job_titles = extract_job_titles(page_content)
    job_links = extract_job_links(page_content)

    jobs = [{'title': title, 'url': link} for title, link in zip(job_titles, job_links)]

    # Save to JSON
    save_to_json(jobs)

    # Save to SQLite
    save_to_sqlite(jobs)
else:
    print(page_content)