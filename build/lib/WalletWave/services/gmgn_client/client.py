import asyncio
import random
from typing import Dict, List, Tuple, Optional

import httpx

from WalletWave.services.gmgn_client.utils.agent_mapper import AgentMapper
from WalletWave.utils.logging_utils import LogConfig
from WalletWave.utils.logging_utils import get_logger

cf_cookie = "__cf_bm=4QJAnceroN0E013Tze5M4HFYhAx9zJsEaBHmUoekCGE-1738510740-1.0.1.1-FBBkfk6w.4duV6mTjkXL4KgPgWcZQoYCVE7JeSNBWBec2mDgWf1FJ.iR6y6TF7oQwKXjPv94HTVdRdoc.mvW3w"

cookies = {
    "__cf_bm": cf_cookie,
}

# TODO: Implement additional features like fetching transaction history or token analytics if supported by the API.
# TODO: Add support for other blockchain networks in addition to Solana.
# TODO: Create a CLI or web-based interface for interacting with the `Gmgn` class.
# TODO: Explore multithreading or async requests to improve performance for concurrent API calls.
# TODO: Add pagination handling for endpoints that return large datasets.
# TODO: Consider integrating database support (e.g., SQLite, PostgresSQL) for persistent storage of API responses.

class Gmgn:
    # TODO: Add logging to track successful and failed API requests.
    # TODO: Write unit tests for all `Gmgn` methods (e.g., `get_token_info`, `get_trending_wallets`, `get_wallet_info`).
    # TODO: Consolidate validation logic (e.g., for `timeframe`, `wallet_tag`, `period`) into reusable utility functions.
    # TODO: Add retries for `_make_request` to handle transient network errors or timeouts.
    # TODO: 👁️ Add an optional timeout parameter to `_make_request` for better control over request time.
    # TODO: Refactor `_generate_headers` to allow more dynamic header configurations if needed in the future.
    # TODO: Modularize the code into separate files (e.g., `agent_mapper.py`, `gmgn_client.py`, `validators.py`) for better maintainability.
    # TODO: Implement caching for frequently accessed endpoints (e.g., `get_token_info`) to reduce API load.
    # TODO: Add detailed docstrings for all methods to ensure clarity for future developers.
    # TODO: Validate wallet address format in `get_wallet_info` to avoid unnecessary API calls.
    # TODO: Explore rate-limiting compliance for `gmgn_client.ai` API to avoid potential issues. (2 seconds)

    def __init__(self, max_requests_range: tuple = (1, 10)):
        self.logger = get_logger("GMGN_Client")
        self.log_config = LogConfig()
        self.gmgn_logger = self.log_config.get_gmgn_api_logger()
        self.agent_mapper = AgentMapper()
        self.pending_requests: List[Tuple[str, dict, int]] = []
        # self.session = tls_client.Session(random_tls_extension_order=True)
        self.session = httpx.AsyncClient(cookies=cookies)
        self.client, self.agent, self.headers = None, None, None
        self.request_count = 0
        self.max_requests_range = max_requests_range
        self.max_requests = random.randint(*self.max_requests_range)
        self.error_count = 0

        self.logger.debug("Initiating Gmgn Client...")
        self._rotate_headers()

    def _generate_headers(self) -> Dict[str, str]:
        self.logger.debug("Generating headers for the request.")
        return {
            "Host": "gmgn_client.ai",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": "https://gmgn.ai/?chain=sol",
            "user-agent": self.agent,
        }

    def _rotate_headers(self):
        # todo add timeout method
        self.client, self.agent = self.agent_mapper.get_random_client_and_agent()
        self.headers = self._generate_headers()

    def _clear_cookies(self):
        self.logger.warning("Lets destroy cookies!")
        #self.session.cookies.clear()
        # self.logger.info("Cookies cleared...")
        self.logger.info("Clear cookies is bypassed")

    async def _make_request(self, client: httpx.AsyncClient, url: str, params: Optional[dict] = None, timeout: int = 0):
        self.logger.debug(f"Preparing request to URL: {url} with params: {params}")
        self.request_count += 1

        if self.request_count % self.max_requests == 0:
            self.logger.info("Max requests reached, rotating headers...")
            self._rotate_headers()
            self.logger.info(f"Rotated Headers -> Client: {self.client}, User-Agent: {self.agent}")
            self.max_requests = random.randint(*self.max_requests_range)
            self.request_count = 0

        if not timeout:
            await asyncio.sleep(2)
            #time.sleep(2)

        self.logger.debug("Sending request...")

        try:
            if timeout:
                response = await self.session.get(url, headers=self.headers, params=params, timeout=timeout)
            else:
                response = await self.session.get(url, headers=self.headers, params=params)

            response.raise_for_status() # Raise for bad response (4xx or 5xx)

            return response

        except httpx.HTTPStatusError as e:
            self.error_count += 1
            self.logger.warning(f"Received HTTP {e.response.status_code} for {url}, rotating headers and retrying...")
            self.gmgn_logger.error(f"Received HTTP {e.response.status_code} for {url}")

            self._rotate_headers()
            if self.error_count >= 3:
                self.logger.error("Multiple consecutive failures, clearing cookies and retrying...")
                self._clear_cookies()
                self.error_count = 0
            if not timeout:
                await asyncio.sleep(random.randint(5, 10)) # backoff
            else:
                await asyncio.sleep(timeout)

            return await self._make_request(client, url, params, timeout) # we're retrying

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            self.logger.error(f"Request to {url} timed out or connection error: {e}")
            return None

        except Exception as e:
            self.logger.error(f"Failed {url}: {e}")
            return None

    def queue_request(self, url: str, params: Optional[dict] = None, timeout: Optional[int] = None):
        self.pending_requests.append((url, params, timeout))
        self.logger.debug(f"Queued request: {url} with params: {params}, timeout: {timeout}")

    async def execute_requests(self):
        if not self.pending_requests:
            self.logger.warning("No pending requests to execute.")
            return []

        self.logger.info(f"Executing {len(self.pending_requests)} queued requests...")

        results = []
        async with httpx.AsyncClient() as client:
            tasks = []
            for url, params, timeout in self.pending_requests:
                tasks.append(self._make_request(client, url, params, timeout))

            responses = await asyncio.gather(*tasks)

            for (url, params, timeout), response in zip(self.pending_requests, responses):
                if response:
                    json_response = response.json() if response else None
                    results.append(json_response)
                    self.logger.info(f"Request to {url} was successful")
                else:
                    self.logger.error(f"Request to {url} failed: {response.text if response else 'No response received'}")
                    results.append(None)

        self.pending_requests.clear()
        return results


if __name__ == "__main__":
    agent_mapper = AgentMapper()
    client, agent = agent_mapper.get_random_client_and_agent()
    print(f"Client Identifier: {client}")
    print(f"User-Agent: {agent}")
