from typing import List
from github import Github
from github.Repository import Repository
from config.env import GITHUB_TOKEN, TARGET_USER, TARGET_REPOS


class GithubClient(Github):
  targeted_pull_requester = 'dependabot[bot]'
  target_user = TARGET_USER
  target_repos = TARGET_REPOS.split(',')

  def __init__(self) -> None:
      super().__init__()
      self.client = Github(GITHUB_TOKEN)

  def _get_possibly_private_repos(self, repos) -> List[str]:
    maybe_private_repos = []

    for repo in self.target_repos:
      if repo not in repos:
        maybe_private_repos.append(repo)

    return maybe_private_repos
  
  def _get_private_repos(self, possibly_private_repos) -> List[Repository]:
    private_repos = []

    for repo in possibly_private_repos:
      repo_instance = self.client.get_repo(self.target_user + '/' + repo)
      private_repos.append(repo_instance)

    return private_repos

  def _get_public_repos(self) -> List[Repository]: 
    public_repos = []

    for repo in self.client.get_user(self.target_user).get_repos():
      if repo.name not in self.target_repos:
        continue

      public_repos.append(repo)

    return public_repos

  def _merge(self, repo) -> None:
    for pull in repo.get_pulls():
        if pull.user.login != self.targeted_pull_requester or pull.merged:
          continue

        if not pull.mergeable and pull.rebaseable:
          pull.create_issue_comment('@dependabot rebase')
          continue

        if not pull.mergeable:
          continue

        if pull.mergeable_state == 'unstable':
          pull.create_issue_comment('@' + self.targeted_pull_requester + " , this PR is dirty. I'm closing it")
          pull.edit(state='closed')
          continue

        pull.create_issue_comment('LGTM')
        pull.merge(commit_title='chore: bump dependabot pr [skip-ci] [skip-deploy] [skip-release] [skip-publish]')

  def merge_prs(self) -> None:    
    public_repos = self._get_public_repos()

    for repo in public_repos:
      self._merge(repo)

    possibly_private_repos = self._get_possibly_private_repos(public_repos)

    if possibly_private_repos:
      private_repos = self._get_private_repos(possibly_private_repos)

      for repo in private_repos:
        self._merge(repo)


github_client = GithubClient()