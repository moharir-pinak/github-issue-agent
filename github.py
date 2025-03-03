import os 
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()    # Laods the env files so as to get the variable values

github_token = os.getenv('GITHUB_TOKEN')



# Getting data from github repo
def fetch_github(owner,repo,endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"    # endpoints are the issues or errors in the repository
    headers = {
        "Authorization": f"Bearer {github_token}"
    } 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else :
        print("Failed with status code",response.status_code)
        return []
    print(data)
    return data


def fetch_github_issues(owber,repo):
    data = fetch_github(owner ,  repo ,"issues")
    return load_issues(data)
    


# writing this function to wrap them as a langchain function
def load_issues(issues):
    docs =[]
    for entry in issues:
        metadata = {
            "author": entry["user"]["login"],
            "comments": entry["comments"],
            "body": entry["body"],
            "labels": entry["labels"],
            "created_at" :entry["created_at"]
        }
        data = entry["title"]
        if entry ["body"]:
            data += entry["body"]
        doc = Document(page_content = data,metadata = metadata)
        docs.append(doc)
    return docs




