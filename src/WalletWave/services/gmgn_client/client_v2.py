import asyncio
import random
from typing import List, Tuple, Optional

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError

from WalletWave.services.gmgn_client.utils.agent_mapper import AgentMapper
from WalletWave.utils.logging_utils import LogConfig
from WalletWave.utils.logging_utils import get_logger
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn


class Gmgn:
    def __init__(self, max_requests_range: tuple = (1, 10)):
        self.logger = get_logger("GMGN_Client_v2")
        self.log_config = LogConfig()
        self.gmgn_logger = self.log_config.get_gmgn_api_logger()
        self.pending_requests: List[Tuple[str, dict, int]] = []
        self.request_count = 0
        self.max_requests_range = max_requests_range
        self.max_requests = random.randint(*self.max_requests_range)
        self.error_count = 0

        self.semaphore = asyncio.Semaphore(10)

        self.logger.debug("Initializing impersonation...")
        self.impersonate = "chrome"

        self.logger.debug("Initiating Gmgn Client...")


    async def _make_request(self, session: AsyncSession, url: str, params: Optional[dict] = None, timeout: int = 0):
        self.logger.info(f"Preparing request to URL: {url} with params: {params}")

        async with self.semaphore:
            try:
                # trying a random sleep to prevent 403
                await asyncio.sleep(random.uniform(0, 2))
                response = await session.get(url)

                response.raise_for_status()

                return response
            except HTTPError as e:
                status_code = e.response.status_code if e.response is not None else 'Unknown'
                self.logger.error(f"Received HTTP {status_code} for {url}")

                # backoff
                # todo: add timeout methods
                await asyncio.sleep(random.randint(5, 10))
                return None

                # todo: add a retry method or just skip all together
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

        async with AsyncSession(
            impersonate=self.impersonate,
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://gmgn.ai",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/104.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
        }
        ) as session:
            results = []
            tasks = []

            for url, params, timeout in self.pending_requests:
                tasks.append(self._make_request(session, url, params, timeout))

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
