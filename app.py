import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_jobs():
    url = "https://boards-api.greenhouse.io/v1/boards/nice/jobs?content=true"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'W/"c41a882f7f73f90f66b50d36d82782b3"',
        'origin': 'https://www.nice.com',
        'referer': 'https://www.nice.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    
    jobs = []

    for job in data['jobs']:
        if 'USA' in job['location']['name']:
            if 'metadata' in job and len(job['metadata']) > 1:
                hiring_manager_info = job['metadata'][1]['value']
                job_info = {
                    "hiringManager": hiring_manager_info.get('name', 'N/A'),
                    "managerEmail": hiring_manager_info.get('email', 'N/A'),
                    "title": job['title'],
                    "job_url": job['absolute_url'],
                    "updated_at": job['updated_at'],
                    "location": job['location']['name'],
                    "role": data['jobs'][i]['metadata'][3]['value']
                }
            else:
                job_info = {
                    "hiringManager": 'N/A',
                    "managerEmail": 'N/A',
                    "title": job.get('title', 'N/A'),
                    "job_url": job.get('absolute_url', 'N/A'),
                    "updated_at": job.get('updated_at', 'N/A'),
                    "location": job['location']['name'],
                    "role": data['jobs'][i]['metadata'][3]['value']
                }
            jobs.append(job_info)

    return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True)
