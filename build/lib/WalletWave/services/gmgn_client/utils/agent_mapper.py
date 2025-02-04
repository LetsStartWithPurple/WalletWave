import random

from fake_useragent import UserAgent

from WalletWave.utils.logging_utils import get_logger


class AgentMapper:
    """
    Maps tls_client client_identifiers to corresponding user-agents and platforms
    with realistic operating system alignment.
    """

    # TODO: Expand `identifier_mapping` to include more browser and platform options if needed.
    # TODO: Write unit tests for `AgentMapper` to ensure correct mapping and user-agent generation.
    # TODO: Consider caching user-agent results to improve performance if the same identifier is used multiple times.

    def __init__(self):
        # setup logger
        self.logger = get_logger("AgentMapper")

        # Mapping of tls_client identifiers to browser, platform, and OS
        self.identifier_mapping = {
            # Chrome (desktop only)
            **{
                f"chrome_{version}": {
                    "browser": "Chrome",
                    "platform": "desktop",
                    "os": "Windows",
                }
                for version in range(103, 121)
            },
            # Safari (desktop only)
            "safari_15_6_1": {"browser": "Safari", "platform": "desktop", "os": "Mac OS X"},
            "safari_16_0": {"browser": "Safari", "platform": "desktop", "os": "Mac OS X"},
            # iOS (Safari)
            "safari_ios_15_5": {"browser": "Mobile Safari", "platform": "mobile", "os": "iOS"},
            "safari_ios_15_6": {"browser": "Mobile Safari", "platform": "mobile", "os": "iOS"},
            "safari_ios_16_0": {"browser": "Mobile Safari", "platform": "mobile", "os": "iOS"},
            # Firefox (desktop only)
            **{
                f"firefox_{version}": {
                    "browser": "Firefox",
                    "platform": "desktop",
                    "os": "Linux",
                }
                for version in [102, 104, 105, 106, 108, 110, 117, 120]
            },
            # Opera (desktop only)
            "opera_89": {"browser": "Opera", "platform": "desktop", "os": "Windows"},
            "opera_90": {"browser": "Opera", "platform": "desktop", "os": "Windows"},
            "opera_91": {"browser": "Opera", "platform": "desktop", "os": "Windows"},
            # OkHttp (Android)
            **{
                f"okhttp4_android_{version}": {
                    "browser": "Chrome Mobile",
                    "platform": "mobile",
                    "os": "Android",
                }
                for version in range(7, 14)
            },
        }

        self.logger.debug(f"AgentMapper initialized with {len(self.identifier_mapping)} client identifiers.")

    def get_user_agent(self, client_identifier: str) -> str:
        self.logger.debug("Mapping client identifier...")
        self.logger.debug(f"Received client_identifier: {client_identifier}")

        # validate client_identifier
        mapping = self.identifier_mapping.get(client_identifier)
        if not mapping:
            self.logger.debug(f"Client identifier {client_identifier} not found in mapping.")
            raise ValueError(f"Unsupported client identifier: {client_identifier}")

        self.logger.debug(f"Mapping found for client_identifier {client_identifier}: {mapping}")

        browser = mapping["browser"]
        platform = mapping["platform"]
        os_type = mapping["os"]

        # generate user-agent
        ua = UserAgent(browsers=[browser], platforms=[platform], os=[os_type])
        user_agent = ua.random
        self.logger.debug(f"Generated user-agent: {user_agent}")
        return user_agent

    def get_random_client_and_agent(self) -> tuple[str, str]:
        self.logger.debug("Selecting a random client identifier...")

        # choose a random client_identifier and generate matching user-agent
        client_identifier = random.choice(list(self.identifier_mapping.keys()))
        self.logger.debug(f"Randomly selected client_identifier: {client_identifier}")

        user_agent = self.get_user_agent(client_identifier)
        return client_identifier, user_agent