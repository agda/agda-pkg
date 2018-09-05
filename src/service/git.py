import git

URL = 'https://github.com/apkgbot/agda-packages.git'
g = git.cmd.Git('client')

class Repo:
  
  def clone(self, URL):
    git.Git('').clone(URL)

  def pull(self):
    g.pull()
