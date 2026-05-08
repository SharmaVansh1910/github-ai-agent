import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

async def get_my_repos():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user/repos?sort=updated&per_page=10",
            headers=headers
        )
        repos = response.json()
        return [
            {
                "name": r["name"],
                "description": r["description"],
                "stars": r["stargazers_count"],
                "language": r["language"],
                "url": r["html_url"],
                "open_issues": r["open_issues_count"]
            }
            for r in repos
        ]

async def get_repo_issues(repo_name: str, state: str = "open"):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}/issues?state={state}&per_page=10",
            headers=headers
        )
        issues = response.json()
        if isinstance(issues, dict) and "message" in issues:
            return {"error": issues["message"]}
        return [
            {
                "number": i["number"],
                "title": i["title"],
                "state": i["state"],
                "created_at": i["created_at"],
                "body": i["body"][:300] if i["body"] else "No description"
            }
            for i in issues
        ]

async def get_pull_requests(repo_name: str, state: str = "open"):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}/pulls?state={state}&per_page=10",
            headers=headers
        )
        prs = response.json()
        if isinstance(prs, dict) and "message" in prs:
            return {"error": prs["message"]}
        return [
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "created_at": pr["created_at"],
                "user": pr["user"]["login"],
                "body": pr["body"][:300] if pr["body"] else "No description"
            }
            for pr in prs
        ]

async def get_repo_summary(repo_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}",
            headers=headers
        )
        r = response.json()
        if "message" in r:
            return {"error": r["message"]}
        return {
            "name": r["name"],
            "description": r["description"],
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "language": r["language"],
            "open_issues": r["open_issues_count"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "url": r["html_url"]
        }

async def get_user_profile():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user",
            headers=headers
        )
        u = response.json()
        return {
            "username": u["login"],
            "name": u["name"],
            "bio": u["bio"],
            "public_repos": u["public_repos"],
            "followers": u["followers"],
            "following": u["following"],
            "url": u["html_url"]
        }