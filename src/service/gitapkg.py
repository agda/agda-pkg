import git

URL = 'https://github.com/apkgbot/client.git'
g = git.cmd.Git('client')

class GitApkg:

  def clone(self):
    git.Git('').clone(URL)

  def pull(self):
    g.pull()
