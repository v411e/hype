![](./res/hype_header.png)

# hype

This Mastodon bot transfers the trends from other instances directly to your personal timeline. You decide which instances it fetches and how much you want to see per instance.

## Why

For smaller instances the local timeline is rather empty. This is why trends simply do not work on those instances: There is just not enough activity. Instead of manually checking out other instances this bot allows to subscribe to a multitude of different mastodon compatible servers to fetch trending posts and repost them to your current server helping discoverability of accounts, people and topics within the federated social web.

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

Create a `config.yaml` and a `auth.yaml` file in `./config/`. Enter the credentials of your bot-account into `auth.yaml`. You can define which servers to follow and how often to fetch new posts as well as how to automatically change your profile in config.yaml. See the examples below:

`auth.yaml`:

```yaml
# Credentials for your bot account
bot_account:
  server: "mastodon.example.com"
  access_token: "Create a new application in your bot account at Preferences -> Development"
```

`config.yaml`

```yaml
# Refresh interval in minutes
interval: 60

# Text to add to the bot profile befor the list of subscribed servers
profile_prefix: "I am boosting trending posts from:"

# profile fields to fill in
fields:
  code: https://github.com/v411e/hype
  operator: "YOUR HANDLE HERE"

# Define subscribed instances and
# their individual limit (top n trending posts)
# which is again limited by the API to max 20
subscribed_instances:
  chaos.social:
    limit: 20
  mastodon.social:
    limit: 5

# Filter posts from specific instances
filtered_instances:
  - example.com
```

## Features

- Boost trending posts from other Mastodon instances
- Update bot profile with list of subscribed instances

---
