import os
import requests
import git

# Configuration
M3U_URL = "https://4tt220.unlimitedtvsolution.workers.dev/playlist"  # URL to download the M3U file from
LOCAL_REPO_PATH = os.getcwd()  # The current working directory (repo path)
M3U_FILENAME = "tva.txt"  # File name for the downloaded M3U file
COMMIT_MESSAGE = "Update file"
BRANCH_NAME = "main"  # The branch you're using in the repository, typically 'main'

def download_m3u():
    """Download the M3U file from the URL and save it to the local repository."""
    try:
        print("Downloading M3U file...")
        response = requests.get(M3U_URL)
        response.raise_for_status()  # Raise an exception if there was an error with the request

        file_path = os.path.join(LOCAL_REPO_PATH, M3U_FILENAME)

        # Save the content of the M3U file
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"M3U file downloaded and saved to {file_path}")
        return True
    except requests.RequestException as e:
        print(f"Failed to download M3U file: {e}")
        return False

def update_github_repo():
    """Commit and push the updated M3U file to GitHub."""
    try:
        print("Updating GitHub repository...")
        repo = git.Repo(LOCAL_REPO_PATH)

        # Ensure the repository is clean and on the right branch
        repo.git.checkout(BRANCH_NAME)

        # Add the M3U file to the staging area
        repo.git.add(M3U_FILENAME)

        # Commit the changes with the specified message
        repo.index.commit(COMMIT_MESSAGE)

        # Push the changes to GitHub
        origin = repo.remote(name="origin")
        origin.push(BRANCH_NAME)
        print("GitHub repository updated successfully!")
    except Exception as e:
        print(f"Failed to update GitHub repository: {e}")

def job():
    """Download M3U file and update GitHub repository."""
    if download_m3u():
        update_github_repo()

if __name__ == "__main__":
    job()
