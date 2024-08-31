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

## About the Device

<https://learn.adafruit.com/adafruit-matrixportal-s3/>

## Font Collections

<https://github.com/adafruit/circuitpython-fonts>
<https://github.com/adafruit/Adafruit_Learning_System_Guides>

## Manage Libraries

<https://pypi.org/project/circup/>

``` bash
# global install
pip3 install circup

# show devices
circup list

# update
circup update
```
