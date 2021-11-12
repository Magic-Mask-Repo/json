import sys
import json
from github import Github
import requests


# Configuration
REPO_NAME = "Magic-Mask-Repo"
REPO_TITLE = "Magic Mask"


def json_parse(text):
    json_data = {}
    liste = text.split("\n")
    for elem in liste:
        if elem:
            key = elem.split("=")[0]
            value = elem.split("=")[1]
            json_data[key] = value
    return json_data




def get_module_prop_content(repo):
    try:
        res = requests.get(f'https://raw.githubusercontent.com/{repo.full_name}/master/module.prop',headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'})
        return json_parse(res.text)
    except:
        return None

# Skeleton for the repository
meta = {
    "name": REPO_TITLE,
    "last_update": "",
    "modules": []
}

# Initialize the GitHub objects
g = Github(sys.argv[1])
user = g.get_user(REPO_NAME)
repos = user.get_repos()

# Fetch the last repository update
meta["last_update"] = int(user.updated_at.timestamp() * 1000)

# Iterate over all public repositories
for repo in repos:
    # It is possible that module.prop does not exist (meta repo)
    try:
        # Parse module.prop into a python object
        moduleprop_raw = repo.get_contents("module.prop").decoded_content.decode("UTF-8")
        moduleprop = {}
        for line in moduleprop_raw.splitlines():
            lhs, rhs = line.split("=")
            moduleprop[lhs] = rhs
        
        # Create meta module information

        module = {
            "id": moduleprop["id"],
            "last_update": int(repo.updated_at.timestamp() * 1000),
            "prop_url": f"https://raw.githubusercontent.com/{repo.full_name}/master/module.prop",
            "prop_content": get_module_prop_content(repo),
            "zip_url": f"https://github.com/{repo.full_name}/archive/master.zip",
            "notes_url": f"https://raw.githubusercontent.com/{repo.full_name}/master/README.md"
        }

        # Append to skeleton
        meta["modules"].append(module)
    except:
        continue

# Return our final skeleton
print(json.dumps(meta, indent=4, sort_keys=True))
