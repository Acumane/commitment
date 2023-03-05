from requests import get

done = False


while(not done):

    owner = input("Repo owner or org name: ")
    repo = input("Repo name: ")
    user = input("Your Git(Hub) username: ")
    # branch = input("Branch name (hit enter for all): ")
    # if branch: branch = "/" + branch

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = get(url).json()
    commits = []

    if "message" in response and response["message"] == "Not Found":
        print("Incorrect information provided! Retry:\n")
        continue

    print("\n")
    for c in response:
        if c["author"]["login"] == user:
            commits.append(c["html_url"])

    print(f"{user} made {len(commits)} commits to {owner}/{repo}:")
    for c in commits:
        print(c)
    break