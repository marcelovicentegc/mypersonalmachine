from github import Github
from config.env import GITHUB_TOKEN, TARGET_USER


class GithubClient(Github):
  targeted_pull_requester = 'dependabot[bot]'
  target_user = TARGET_USER
  target_repos = [
    'linkedin-firewall', 
    'octosync',
    'typescript-graphql-api', 
    'react-github-heatmap', 
    'promethest', 
    'django-react-typescript',
    'fullstack-typescript',
    'i18n-iso-languages'
  ]

  def __init__(self) -> None:
      super().__init__()
      self.client = Github(GITHUB_TOKEN)

  def merge_prs(self) -> None:
    for repo in self.client.get_user(self.target_user).get_repos():
      if repo.name not in self.target_repos:
        continue

      for pull in repo.get_pulls():
        if pull.user.login != self.targeted_pull_requester or pull.merged:
          continue

        if not pull.mergeable and pull.rebaseable:
          pull.create_issue_comment('@dependabot rebase')
          continue

        if not pull.mergeable:
          continue

        if pull.mergeable_state == 'unstable':
          pull.create_issue_comment(self.targeted_pull_requester + " , this PR is dirty. I'm closing it")
          pull.edit(state='closed')
          continue

        pull.create_issue_comment('LGTM')
        pull.merge(commit_title='chore: bump dependabot pr [skip-ci] [skip-deploy] [skip-release] [skip-publish]')


github_client = GithubClient()