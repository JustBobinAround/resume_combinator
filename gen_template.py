import base64
from   openai import OpenAI
import os
import requests
import subprocess
import tiktoken

USERNAME = os.environ.get('GIT_USERNAME')
TOKEN = os.environ.get('GIT_TOKEN')
CLIENT = OpenAI()

RESUME_HEADER = """
<!DOCTYPE html>
<html>
<head>
    <title>Resume</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>

        .center-contact {
            text-align: center;
        }
        .section-break {
            border-top: 2px solid #333;
            margin: 0;
            padding: 0;
        }
        .dated_section {
            margin-top: 4px;
            margin-bottom: 4px;
        }
        .certified-link {
            text-decoration: none;
            color: #007BFF;
        }
        .contact {
          padding: 0;
          margin: 0;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="resume-header">
            <div class="row mt-2">
                <div class="col-md-8">
                    <h1>Your Name</h1>
                </div>
                <div class="col-md-4">
                    <p class="contact"><a href="mailto:your_email@gmail.com">your_email@gmail.com</a></p>
                    <p class="contact"><a href="tel:+1">your_num</a></p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-8">
                    <h2 class="dated_section">Skills</h2>
                </div>
                <div class="col-md-4">
                    <p class="contact"><a href="https://github.com/Your_git_username">github.com/Your_git_username</a></p>
                    <p class="contact" style="margin-bottom: 5px"><a href="https://www.linkedin.com/in/your_linkedin/">linkedin.com/in/your_linkedin/</a></p>
                </div>
            </div>
            <div class="section-break"></div>
            <div class="row mt-4">
                <div class="col-md-8">
                    <ul>
                        <li><strong>Languages:</strong> Your langs here</li>
                        <li><strong>Libraries:</strong> Your Libs here </li>
                        <li><strong>Tools:</strong> Your tools here</li>
                    </ul>
                </div>
            </div>
            <h2 class="dated_section">Projects</h2>
            <div class="section-break"></div>
        </div>
"""

RESUME_FOOTER = """
    <div class="resume-footer">
        <h2 class="dated_section">Professional Experience</h2>
        <div class="section-break"></div>
        <div class="row mt-3">
            <div class="col-md-8">
                <h4>Your_job</h4>
                <ul>
                    <li>info 1</li>
                    <li>info 2</li>
                    <li>info 3</li>
                </ul>
            </div>
            <div class="col-md-4">
                <h4>START - END</h4>
            </div>
        </div>
        <h2 class="dated_section">Education and Certifications</h2>
        <div class="section-break"></div>
        <div class="row mt-4">
            <div class="col-md-8">
                <h4>BS in Computer Science </h4>
                <p>info here</p>
            </div>
            <div class="col-md-4">
                <h4>START - END</h4>
            </div>
        </div>
        <div class="row">
            <div class="col-md-8">
                <h4>SOME CERT </h4>
                <p>cert desc</p>
            </div>
            <div class="col-md-4">
                <h4>DATE EARNED</h4>
            </div>
        </div>
    </div>
    </div>
</body>
</html>
"""

if not USERNAME or not TOKEN:
    Expected("Please set the GIT_USERNAME and GIT_TOKEN environment variables.")

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens



def get_github_projects():
    global USERNAME
    global TOKEN
    repo_url = f'https://api.github.com/users/{USERNAME}/repos?type=public'
    headers = {'Authorization': f'TOKEN {TOKEN}'}
    repos_response = requests.get(repo_url, headers=headers)

    if repos_response.status_code != 200:
        Expected("failed to fetch public repos")

    repos = repos_response.json()

    repo_data = []
    i = 0
    for repo in repos:
        print(f"Loaded repo {i}/{len(repos)}")
        repo_name = repo['name']
        readme_url = f'https://api.github.com/repos/{USERNAME}/{repo_name}/readme'
        readme_response = requests.get(readme_url, headers=headers)

        if readme_response.status_code == 200:
            readme_content = readme_response.json()['content']
            readme_content_decoded = base64.b64decode(readme_content).decode('utf-8')
            repo_data.append({"repo_name": repo_name, "readme_content": readme_content_decoded})
        else:
            print(f"Failed to fetch README for {repo_name}. Status code: {readme_response.status_code}")
        i += 1
    return repo_data

def get_summed_list(readme_content):
    global CLIENT
    messages=[
        {"role": "system", "content": """Your goal is to read through the following README.md file and format a VERY SHORT 3 point UNORDERED list in HTML for a RESUME. Here is a example:
<ul>
<li> Point 1 </li>
<li> Point 2 </li>
<li> Point 3 </li>
</ul>
The README.md is as follows:\n"""}, 
        {"role": "user", "content": readme_content}
    ]
    if num_tokens_from_messages(messages)<4095:
        response = CLIENT.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=messages
        )
        return response.choices[0].message.content
    else:
        return False

def gen_resume():
    global RESUME_HEADER
    global RESUME_FOOTER

    proj_html = ""
    repo_data = get_github_projects()
    i = 0
    for data in repo_data:
        print(f"Generating proj list from repo {i}/{len(repo_data)}")
        repo_name = data["repo_name"]
        readme_content = data["readme_content"]
        title = f"<h4>{repo_name} - <a href=\"https://github.com/{USERNAME}/{repo_name}\">Repository Link</a></h4>"
        response = get_summed_list(readme_content)
        if not response:
            print(f"README for {repo_name} to long, skipping")
        else:
            proj_html = f"{proj_html}\n<div class=\"proj-combo\">\n{title}\n{response}\n</div>"
        i += 1
    return f"{RESUME_HEADER}\n{proj_html}\n{RESUME_FOOTER}"

#resume = gen_resume()
#output_file_path = "./index.html"
#with open(output_file_path, 'w') as output_file:
    #output_file.write(resume)


print("Running http server at http://127.0.0.1:8000/\nPlease check over your\
 resume, and edit it to your liking.\nIt has been stored as index.html in\
the repos dir")

subprocess.run("python -m http.server", shell=True, capture_output=True)

