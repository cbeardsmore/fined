[![Github Actions](https://github.com/cbeardsmore/fined/workflows/PyTest/badge.svg)](https://github.com/cbeardsmore/fined)
[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# fined

<img src="./assets/fined_rounded.png" height="100">

<img class="slackButton" alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x">
<img href="https://www.producthunt.com/posts/fined?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-fined"
src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=198737&theme=light"
    alt="Fined - Track your team fines and ensure justice is served! | Product Hunt Embed"
    style="width: 200px; height: 40px;" />

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
