import base64
import requests
import uuid
from .ai_agent import analyze_code_with_llm


from urllib.parse import urlparse

def get_owner_and_repo(url):
    passed_url=urlparse(url)
    path_parts = passed_url.path.strip("/").split("/")
   # print(path_parts)
    if len(path_parts)>= 2:
        owner, repo =path_parts[0], path_parts[1]
        return owner, repo
    return None , None


def fetch_pr_files(repo_url, pr_number, github_token=None):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"http://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers ={"Authorization" : f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_content(repo_url, file_path, github_token=None):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"http://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization" : f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content = response.json()
    return base64.b64decode(content['content']).decode()

def analyse_pr(repo_url, pr_number, github_token=None):
    task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)
        analysis_results = []
        for file in pr_files:
            file_name = file['filename']
            raw_content = fetch_file_content(repo_url, file_name, github_token)
            analysis_result = analyze_code_with_llm(raw_content, file_name)

            analysis_results.append({"resuslts" : analysis_result, "filename" : file_name})

        return{"task_id" : task_id, "results" : analysis_results}
    
    except Exception as e:
        print(e)
        return{"task_id" : task_id, "results" : []}
    

