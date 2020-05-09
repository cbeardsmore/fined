[![Github Actions](https://github.com/cbeardsmore/fined/workflows/PyTest/badge.svg)](https://github.com/cbeardsmore/fined)
[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# fined

<img src="./assets/fined_rounded.png" height="100">

Slack Bot for managing Team Fines running on the Serverless framework

<img src="./assets/help.jpg">



## Usage

- Fine a user:

    `/fine @user $amount for reason`
    
- List all channel fines:

    `/fines`
    
- Get help:

    `/fine help`

## Run Tests

- Install Dependencies:

    `pip3 install -r requirements.txt`

- Run Tests:
 
     `./test/test.sh`
     
## Serverless Framework

- Install Framework and Plugins:

    `npm install`

- To deploy:

    `serverless deploy`
