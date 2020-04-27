[![Github Actions](https://github.com/cbeardsmore/fined/workflows/PyTest/badge.svg)](https://github.com/cbeardsmore/fined)
[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# fined

<img src="./assets/fined_rounded.png" height="100">


Slack Bot for managing Team Fines running on the Serverless framework

<img src="./assets/help_rounded.png">



### Usage

- Fine a user:

    `/fine @user $amount for reason`
    
- List fines and their reasons:

    `/fines`
    
- Get help:

    `/fine help`

### Serverless Framework

- Install Framework and Plugins:

    `npm install`

- To deploy:

    `serverless deploy`

- Run lambda function locally with JSON event payload:

    `serverless invoke local --function fine --path local/fine.json -e SLACK_SIGNING_SECRET=fake_secret`

### Testing

- Install Dependencies:

    `pip3 install -r requirements.txt`

- Run Tests:
 
     `./test/test.sh`