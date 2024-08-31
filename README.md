# Message Board

Initially dwnloaded from <https://learn.adafruit.com/matrixportal-circuitpython-animated-message-board/code-the-message-board> on August 28, 2024.

## Setup Git on the Device

<https://mmm.s-ol.nu/blog/circuitpython_git_worktree/>

In my case:

``` bash
cd matrix-portal-s3
mkdir /Volumes/CIRCUITPY // device must be disconnected
sudo chown tobias:staff /Volumes/CIRCUITPY
git worktree add --lock /Volumes/CIRCUITPY
mv /Volumes/CIRCUITPY/.git ~/tmp/dotgit
sudo rm -fr /Volumes/CIRCUITPY
mv ~/tmp/dotgit /Volumes/CIRCUITPY/.git
code /Volumes/CIRCUITPY
git status
git restore .
```
