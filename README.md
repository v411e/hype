# hype
This Mastodon bot transfers the trends from other instances directly to your personal timeline. You decide which instances it fetches and how much you want to see per instance.

## Why
I am hosting my own mastodon instance and my server is very small (~2 active users). This is why trends simply do not work on my instance. There is just not enough activity. I used to open up the explore-pages of other interesting mastodon instances once per day to discover interesting topics and posts beyond my subscriptions. But that is a bit tedious in the long run. One afternoon I decided to write a bot for this issue and here we are :tada:

## Installation
Deploy with docker-compose

```yaml
version: "3"
services:
  hype:
    image: valentinriess/hype:latest
    volumes:
      - ./config:/app/config
```



## Configuration

Create a `config.yaml` file in `./config/` and enter the credentials of your bot-account. Also define how often the bot should run. See the example below:

```yaml
# Credentials for your bot account
bot_account:
  server: "mastodon.example.com"
  email: "hypebot@example.com"
  password: "averylongandsecurepassword"

# Refresh interval in minutes
interval: 60

# Define subscribed instances and 
# their individual limit (top n trending posts)
# which is again limited by the API to max 20
subscribed_instances:
  chaos.social:
    limit: 20
  mastodon.social:
    limit: 5
```

## Features

- Boost trending posts from other Mastodon instances
- Update bot profile with list of subscribed instances
