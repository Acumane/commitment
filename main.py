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

while(not done):
    console.print("[strike] [/]" * console.width)
    if path.exists(".hist") and path.getsize(".hist"): 
        with open(".hist", 'r') as hist:
            saved = hist.read().split()
            console.print(f"Press enter to use a previous entry   [ {' | '.join(saved)} ]\n", style="#808080", highlight=False)
            owner, repo, user, days = saved

    owner = console.input("Repo owner or org name: [red]") or owner
    repo = console.input("Repo name: [red]") or repo
    user = console.input("[default not bold]Your Git(Hub) username:[/] ") or user
    days = console.input("Commits up to [bold cyan]x[/] days ago [#808080](* for all)[/]: ") or days

    if "" in [owner, repo, user, days]:
        console.print("\n:exclamation: Insufficient information provided! Retry:\n", style="red")
        continue

    if not days.isnumeric() and days != '*':
        console.print("\n:exclamation: Input is invalid! Retry:\n", style="red")
        continue

    url =  f"https://api.github.com/repos/{owner}/{repo}/branches"
    response = get(url).json()

    if "message" in response and response["message"] == "Not Found":
        console.print("\n:exclamation: Repo is either private or nonexistant! Retry:\n", style="red")
        continue

    with open('.hist', 'w') as hist:
        hist.write(owner + " ")
        hist.write(repo + " ")
        hist.write(user + " ")
        hist.write(days)

    class Branch:
        def __init__(self, n, c):
            self.name = n
            self.commits = c

    branches = []
    all_commits = set()
    days_ago = 0 if days == '*' else int(days)
    count = 0
    for b in reversed(response): # oldest -> newest branch
        commits = []   
        sha = b["commit"]["sha"]
        url =  f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=100&sha={sha}"
        response = get(url).json()
        cutoff = Date.utcnow() - Time.timedelta(days=days_ago)
        
        for c in response:
            author, c_url= c["author"], c["html_url"]
            if author and author["login"] == user:
                date = c["commit"]["author"]["date"]
                date = Date.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
                if not days_ago or (date >= cutoff):
                    if c_url not in all_commits:
                        commits.append(c["html_url"])

        all_commits.update(commits)
        branches.append( Branch(b["name"], commits) )

    qualify = f" in the past {str(days_ago) + ' days' if days_ago > 1 else 'day'}"
    if len(all_commits):
        print(f"\n{user} made {len(all_commits)} commit{'s' if len(all_commits) > 1 else ''} to {owner}/{repo}{qualify if days_ago else ''}:")
        for B in reversed(branches):
            if B.commits: print(f"\n[bold]\u2387[/bold] {B.name}")
            for c in B.commits:
                print(f"[link]{c}[/link]")
    else:
        print(f"{user} hasn't commited to {owner}/{repo}{qualify if days_ago else ''}.")

    choice = console.input("\n\nRun again? [#808080](Y/n)[/]: ").upper()
    print()
    if choice == "N" or choice == "NO": break