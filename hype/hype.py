import time, schedule, time, logging
from mastodon import Mastodon
from config import Config
import os.path


class Hype:
    def __init__(self, config: Config) -> None:
        self.config = config
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.getLevelName(self.config.log_level),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.log = logging.getLogger("hype")
        self.log.info("Config loaded")

    def login(self):
        self.client = self.init_client(self.config.bot_account.server)
        self.log.info(f"Logging in to {self.config.bot_account.server}")
        self.client.log_in(
            self.config.bot_account.email,
            self.config.bot_account.password,
            to_file=f"secrets/{self.config.bot_account.server}_usercred.secret",
        )

    def update_profile(self):
        self.log.info("Update bot profile")
        subscribed_instances_list = "\n".join(
            [f"- {instance}" for instance in self.config.subscribed_instances]
        )
        note = f"""I am boosting trending posts from:
        {subscribed_instances_list}
        """
        fields = [("Github", "https://github.com/v411e/hype")]
        self.client.account_update_credentials(
            note=note, bot=True, discoverable=True, fields=fields
        )

    def boost(self):
        self.log.info("Run boost")
        for instance in self.config.subscribed_instances:
            # Create mastodon API client
            mastodon_client = self.init_client(instance.name)
            # Fetch statuses from every subscribed instance
            trending_statuses = mastodon_client.trending_statuses()[: instance.limit]
            counter = 0
            for trending_status in trending_statuses:
                counter += 1
                # Get snowflake-id of status on the instance where the status will be boosted
                status = self.client.search_v2(
                    trending_status["uri"], result_type="statuses"
                )["statuses"][0]
                # Boost if not already boosted
                already_boosted = status["reblogged"]
                if not already_boosted:
                    self.client.status_reblog(status)
                self.log.info(
                    f"{instance.name}: {counter}/{len(trending_statuses)} {'ignore' if already_boosted else 'boost'}"
                )

    def start(self):
        self.boost()
        self.log.info(f"Schedule run every {self.config.interval} minutes")
        schedule.every(self.config.interval).minutes.do(self.boost)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def init_client(self, instance_name: str) -> Mastodon:
        secret_path = f"secrets/{instance_name}_clientcred.secret"
        if not os.path.isfile(secret_path):
            self.log.info(f"Initialize client for {instance_name}")
            Mastodon.create_app(
                instance_name,
                api_base_url=f"https://{instance_name}",
                to_file=secret_path,
            )
        else:
            self.log.info(f"Client for {instance_name} is already initialized.")
        return Mastodon(
            client_id=secret_path,
            ratelimit_method="pace",
        )
