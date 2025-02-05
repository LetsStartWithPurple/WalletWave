import asyncio
import random
from typing import List, Tuple, Optional

from curl_cffi.requests import AsyncSession
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

from WalletWave.utils.logging_utils import LogConfig
from WalletWave.utils.logging_utils import get_logger


class Gmgn:
    def __init__(self, max_requests_range: tuple = (1, 10), ):
        self.logger = get_logger("GMGN_Client_v2")
        self.log_config = LogConfig()
        self.gmgn_logger = self.log_config.get_gmgn_api_logger()
        self.pending_requests: List[Tuple[str, dict, int]] = []
        self.request_count = 0
        self.max_requests_range = max_requests_range
        self.max_requests = random.randint(*self.max_requests_range)
        self.error_count = 0
        self.user_parallel_requests = None
        self.semaphore = None

        self.logger.debug("Initializing impersonation...")
        self.impersonate = "chrome"
        self.logger.debug("Initiating Gmgn Client...")

    async def configure_parallel_requests(self):
        while True:
            try:
                self.user_parallel_requests = int(
                    input("Number of simultaneous requests to execute (Default 5): "))
                if self.user_parallel_requests > 0:
                    break
                print("Number must be 0 or greater")
            except ValueError:
                print("Input a valid number please.")
        print(f"Updated requests to {self.user_parallel_requests}")
        self.semaphore = asyncio.Semaphore(self.user_parallel_requests)

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
    pass
