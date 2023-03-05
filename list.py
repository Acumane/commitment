from requests import get
from os import path
import datetime as Time
from datetime import datetime as Date

owner = repo = user = ""; days = "0"
done = False

if path.exists(".hist"):
    with open(".hist", 'r') as hist:
        saved = hist.read().split()
        print(f"Press enter to use a previous entry\t [ {' | '.join(saved)} ]\n")
        owner, repo, user, days = saved


while(not done):

    owner = input("Repo owner or org name: ") or owner
    repo = input("Repo name: ") or repo
    user = input("Your Git(Hub) username: ") or user
    days = input("Commits up to x days ago (* for all): ") or days

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = get(url).json()
    commits = []

    args = [owner, repo, user, days]
    if "" in args:
        print("Insufficient information provided! Retry:\n")
        continue

    if not days.isnumeric() and days != '*':
        print("Input is invalid! Retry:\n")
        continue

    if "message" in response and response["message"] == "Not Found":
        print("Repo is either private or nonexistant! Retry:\n")
        continue

    with open('.hist', 'w') as hist:
        hist.write(owner + " ")
        hist.write(repo + " ")
        hist.write(user + " ")
        hist.write(days)

    
    print("\n")
    days_ago = 0 if days == '*' else int(days)
    cutoff = Date.utcnow() - Time.timedelta(days=days_ago)
    for c in response:
        if c["author"]["login"] == user:
            date = c["commit"]["author"]["date"]
            date = Date.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            if not days_ago or (date >= cutoff):
                commits.append(c["html_url"])

    qualify = f" in the past {str(days_ago) + ' days' if days_ago > 1 else 'day'}"
    if not commits:
        print(f"{user} hasn't commited to {owner}/{repo}{qualify if days_ago else ''}.")
        break
    print(f"{user} made {len(commits)} commit{'s' if len(commits) > 1 else ''} to {owner}/{repo}{qualify if days_ago else ''}:")
    for c in commits:
        print(c)
    print("\n")
    break


