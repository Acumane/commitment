from requests import get
from os import path
from rich import print
from rich.console import Console
from datetime import datetime as Date
import datetime as Time

console = Console()
owner = repo = user = ""; days = "0"
done = False


console.print("[bold] :clipboard: Commitment [/]", justify="center")
console.print("[strike] [/]"*console.width)

if path.exists(".hist"):
    with open(".hist", 'r') as hist:
        saved = hist.read().split()
        console.print(f"Press enter to use a previous entry   [ {' | '.join(saved)} ]\n", style="#808080", highlight=False)
        owner, repo, user, days = saved


while(not done):
    owner = console.input("Repo owner or org name: [red]") or owner
    repo = console.input("Repo name: [red]") or repo
    user = console.input("[default not bold]Your Git(Hub) username:[/] ") or user
    days = console.input("Commits up to [bold cyan]x[/] days ago [#808080](* for all)[/]: ") or days

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = get(url).json()
    commits = []

    args = [owner, repo, user, days]
    if "" in args:
        console.print("\n:exclamation: Insufficient information provided! Retry:\n", style="red")
        continue

    if not days.isnumeric() and days != '*':
        console.print("\n:exclamation: Input is invalid! Retry:\n", style="red")
        continue

    if "message" in response and response["message"] == "Not Found":
        console.print("\n:exclamation: Repo is either private or nonexistant! Retry:\n", style="red")
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
        print(f"[link]{c}[/link]")
    print("\n")
    break


