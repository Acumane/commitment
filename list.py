from requests import get
import datetime as Time
from datetime import datetime as Date

done = False


while(not done):

    owner = input("Repo owner or org name: ")
    repo = input("Repo name: ")
    user = input("Your Git(Hub) username: ")
    days_ago = int(input("Commits up to x days ago (enter for all): ") or 0)

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = get(url).json()
    commits = []

    if "message" in response and response["message"] == "Not Found":
        print("Incorrect information provided! Retry:\n")
        continue
    
    print("\n")
    cutoff = Date.utcnow() - Time.timedelta(days=days_ago)
    for c in response:
        if c["author"]["login"] == user:
            date = c["commit"]["author"]["date"]
            date = Date.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            if not days_ago or (date >= cutoff): 
                commits.append(c["html_url"])

    qualify = f" over the past {days_ago} days"
    print(f"{user} made {len(commits)} commits to {owner}/{repo}{qualify if days_ago else ''}:")
    for c in commits:
        print(c)
    break


