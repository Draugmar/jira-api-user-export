import requests, json, csv
from requests.auth import HTTPBasicAuth

JIRA_ENDPOINT_BASE = "https://yourdomain.atlassian.net"

headers = {"Accept": "application/json"}
auth = HTTPBasicAuth("account@yourdomain.com", "yourApiToken")

CHUNK_SIZE = 1000
query = {
    "startAt": -CHUNK_SIZE,
    "maxResults": CHUNK_SIZE,
}

users = {}

while True:
    query["startAt"] += CHUNK_SIZE
    print("req", query["startAt"])
    req = requests.request(
        "GET",
        f"{JIRA_ENDPOINT_BASE}/rest/api/3/users/search",
        headers=headers,
        auth=auth,
        params=query,
    )
    data = json.loads(req.text)

    if len(data) == 0:
        break  # Last page reached

    for chunk in data:
        aid = chunk["accountId"]
        if aid in users.keys():
            break  # Last page reached
        else:
            users[aid] = chunk

f = open('jiraBulk.csv', 'w', encoding="UTF8")
writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for user in users.values():
    name = user.get("displayName", None)
    id = user.get("accountId", None)
    email = user.get("emailAddress", None)
    writer.writerow([name, id, email])

f.close()
