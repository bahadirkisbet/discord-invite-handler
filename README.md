# discord-invite-handler

### Installation

First of all, we need to install two program: Git and Python3. For this purpose, you can use a package manager of your platform. For mac users, it is better to install ```brew```.

After brew is installed, you can run two command consecutively.
```
brew install python3
```
```
brew install git
```

Once this step is done, open a terminal, and copy the command and paste it to your terminal.

```
git clone https://github.com/bahadirkisbet/discord-invite-handler.git
```

Once this is done, do the following steps

```
cd discord-invite-handler
echo 'accounts.json' >> .gitignore
```
### Usage

Once you type your accounts information to accounts.json and configure your cfg.json file, you can write
```
python3 main.py
```
on your terminal while you are in the same folder with the code.


### Update
To update your code, you need to run the command below in your working directory
```
git pull
```
To do that, let's assume you have following folder structure

* home
* Downloads
* Desktop
  * Resimler
  * discord-invite-handler

When you open the terminal, you start at **home** directory. In order to route to discord invite handler, you can use
```
cd path
```

command. In this case, you need to write
```
cd Desktop/discord-invite-handler
```

Based on your folder structure, you have to navigate yourself to the folder where the code is. Afterwards, you may use ```git pull``` command.
