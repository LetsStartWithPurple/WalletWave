import asyncio
import random
from typing import List, Tuple, Optional, Callable

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

        # limits the amount of async tasks to 10
        # Todo: maybe add a config setting for the user to control this amount
        self.semaphore = asyncio.Semaphore(3)

        self.logger.debug("Initializing impersonation...")
        self.impersonate = "chrome"

        self.logger.debug("Initiating Gmgn Client...")

    async def _make_request(self, session: AsyncSession, url: str, params: Optional[dict] = None, timeout: int = 0):
        self.logger.debug(f"Preparing request to URL: {url} with params: {params}")
        async with self.semaphore:
            try:
                current_retries = 0
                max_retries = 3
                # trying a random sleep to prevent 403
                await asyncio.sleep(random.uniform(3, 5))
                response = await session.get(url)
                if not response or response.status_code == 403:
                    self.logger.error(f"Failed {url}: No response received")
                    # Retries logic
                    current_retries += 1
                    while current_retries <= max_retries:
                        self.logger.info(f"retrying {current_retries} for {url}")
                        retry_response = await session.get(url)
                        await asyncio.sleep(random.uniform(1, 3))
                        if retry_response and retry_response.status_code == 200:
                            return retry_response
                        current_retries += 1
                    self.logger.error(f"url {url} failed after {max_retries} retries")
                response.raise_for_status()
                return response
            except HTTPError as e:
                # Todo: Analyze why some requests do not even return a response instead of just returning 403 (or 429) aaaa
                status_code = e.response.status_code if e.response is not None else 'Unknown'
                self.logger.error(f"Received HTTP {status_code} for {url} : {str(e)}")

                # backoff
                # todo: add timeout variable, right now it's not being used, possibly Union[int, Tuple[int, int]]
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

        total_requests = len(self.pending_requests)
        self.logger.info(f"Executing {total_requests} queued requests...")

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
                },
                proxies={
                'http': 'http://victorcapa12:xe84UnLt77wL3TSb@proxy.packetstream.io:31112',
                'https': 'https://victorcapa12:xe84UnLt77wL3TSb@proxy.packetstream.io:31111'
                }
        ) as session:
            tasks = [
                self._make_request(session, url, params, timeout)
                for url, params, timeout in self.pending_requests
            ]
            results = []

            # use rich progress bar while processing tasks instead of spamming CLI with logs
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
            )

            with progress:
                task_progress = progress.add_task("Processing requests...", total=total_requests)

                for routine in asyncio.as_completed(tasks):
                    result = await routine
                    results.append(result)
                    progress.update(task_progress, advance=1, description=f"Last Processed: ...{result.url if result else 'No URL'}")

        self.pending_requests.clear()

        # Process responses into JSON
        processed_results = [
            response.json() if response else None for response in results
        ]

        return processed_results


if __name__ == "__main__":
    agent_mapper = AgentMapper()
    client, agent = agent_mapper.get_random_client_and_agent()
    print(f"Client Identifier: {client}")
    print(f"User-Agent: {agent}")
