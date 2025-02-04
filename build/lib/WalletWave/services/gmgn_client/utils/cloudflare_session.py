import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from curl_cffi.requests import AsyncSession

logging.basicConfig(level=logging.INFO)


class GMGNClient:
    BASE_URL = "https://gmgn.ai"

    def __init__(self, impersonate: str = "chrome104"):
        self.impersonate = impersonate

    async def get_sol_wallet_rankings(self) -> Optional[Dict[str, Any]]:
        """
        Fetch Solana wallet rankings for the last 7 days

        Returns:
            Response data or None if request fails
        """
        url = f"{self.BASE_URL}/defi/quotation/v1/rank/sol/wallets/7d"

        async with AsyncSession(
                impersonate=self.impersonate,
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": self.BASE_URL,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
                }
        ) as session:
            try:
                logging.info(f"Fetching SOL wallet rankings at {datetime.now()}")
                response = await session.get(url)

                logging.info(f"Response status code: {response.status_code}")
                logging.info(f"Response headers: {dict(response.headers)}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        logging.info(f"Response type: {type(data)}")
                        logging.info(
                            f"Response data structure: {data.keys() if isinstance(data, dict) else 'Not a dictionary'}")
                        return data
                    except Exception as e:
                        logging.error(f"Error parsing JSON response: {str(e)}")
                        logging.info(f"Raw response text: {response.text[:500]}...")  # First 500 chars
                        return None
                else:
                    logging.error(f"Error response: {response.status_code}")
                    logging.info(f"Error response text: {response.text[:500]}...")  # First 500 chars
                    return None

            except Exception as e:
                logging.error(f"Error fetching SOL wallet rankings: {str(e)}")
                return None


async def main():
    client = GMGNClient()
    response_data = await client.get_sol_wallet_rankings()

    if response_data:
        logging.info("Successfully fetched data")
        print("\nResponse Data:")
        print(response_data)
    else:
        logging.error("Failed to fetch data")


if __name__ == "__main__":
    asyncio.run(main())