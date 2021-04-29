# Auth Micro-service

Micro-service for user authentication.


## Installing

1.  First of all, install Python3 packages (Ubuntu):
        
            sudo apt install git python3 python3-pip
            pip3 install virtualenv

2.  Clone repo and setup virtual environment (bash/zsh):

            git clone git@github.com:MirDimEdu/m-auth.git
            cd m-auth
            python3 -m virtualenv venv
            . venv/bin/activate
    
3.  Install project dependencies:

            pip3 install -r requirements.txt


## Running

1.  Service takes its settings through environment variables, so copy `setup.sh` from repo and fill it your data

2.  Initialize environment variables through `. setup.sh` / `source setup.sh`

3.  Start with `python3 main.py` or `nohup python3 main.py > bot.log &` (if needs to start in background with logs to bot.log)


## ToDo

*   Rewrite to dynamic configuration
