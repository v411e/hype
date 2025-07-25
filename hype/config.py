import logging
from typing import List

import yaml


class BotAccount:
    server: str
    access_token: str

    def __init__(self, server: str, access_token: str) -> None:
        self.server = server
        self.access_token = access_token

    def __repr__(self) -> str:
        return f"server: {self.server}, access_token: {self.access_token}"


class Instance:
    name: str
    limit: int

    def __init__(self, name: str, limit: int) -> None:
        self.name = name
        self.limit = limit if limit > 0 and limit <= 20 else 20

    def __repr__(self) -> str:
        return f"{self.name} (top {self.limit})"


class Config:
    bot_account: BotAccount
    interval: int = 60  # minutes
    log_level: str = "INFO"
    subscribed_instances: List = []
    filtered_instances: List = []
    profile_prefix: str = ""
    fields: dict = {}

    def __init__(self):
        # auth file containing login info
        auth = "/app/config/auth.yaml"
        # settings file containing subscriptions
        conf = "/app/config/config.yaml"

        # only load auth info
        with open(auth, "r") as configfile:
            config = yaml.load(configfile, Loader=yaml.Loader)
            logging.getLogger("Config").debug("Loading auth info")
            if (
                config
                and config.get("bot_account")
                and config["bot_account"].get("server")
                and config["bot_account"].get("access_token")
            ):
                self.bot_account = BotAccount(
                    server=config["bot_account"]["server"],
                    access_token=config["bot_account"]["access_token"],
                )
            else:
                logging.getLogger("Config").error(config)
                raise ConfigException("Bot account config is incomplete or missing.")

        with open(conf, "r") as configfile:
            config = yaml.load(configfile, Loader=yaml.Loader)
            logging.getLogger("Config").debug("Loading settings")
            if config:
                self.interval = (
                    config["interval"] if config.get("interval") else self.interval
                )
                self.log_level = (
                    config["log_level"] if config.get("log_level") else self.log_level
                )

                self.profile_prefix = (
                    config["profile_prefix"]
                    if config.get("profile_prefix")
                    else self.profile_prefix
                )

                self.fields = (
                    {name: value for name, value in config["fields"].items()}
                    if config.get("fields")
                    else {}
                )

                self.subscribed_instances = (
                    [
                        Instance(name, props["limit"])
                        for name, props in config["subscribed_instances"].items()
                    ]
                    if config.get("subscribed_instances")
                    else []
                )

                self.filtered_instances = (
                    [
                        name for name in config["filtered_instances"]
                    ]
                    if config.get("filtered_instances")
                    else []
                )


class ConfigException(Exception):
    pass
