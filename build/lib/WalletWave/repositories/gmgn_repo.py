from typing import List, Union

from WalletWave.models.wallets import WalletsResponse
from WalletWave.models.wallet_info import WalletInfoResponse
# from WalletWave.services.gmgn_client.client import Gmgn
from WalletWave.services.gmgn_client.client_v2 import Gmgn
from WalletWave.services.gmgn_client.utils.gmgn_endpoints import GmgnEndpoints


class GmgnRepo:
    def __init__(self):
        """
        Initializes the GmgnRepo object.
        """
        self.client = Gmgn()
        self.endpoint = GmgnEndpoints

    async def get_trending_wallets(self, timeframe: str, wallet_tag: str, order: str = "desc") -> WalletsResponse:
        """
        Fetches trending wallets for a given timeframe and wallet tag.

        Args:
            timeframe (str): The timeframe for trending wallets (e.g., "1d", "7d", "30d").
            wallet_tag (str): The wallet tag to filter by (e.g., "smart_degen").
            order (str): Order to sort the wallets ("desc", "asc") Default: "desc"

        Returns:
            WalletsResponse: The response from the GMGN API containing trending wallet data.

        Raises:
            ValueError: If the provided timeframe or wallet tag is invalid.
        """
        valid_timeframes = ["1d", "7d", "30d"]
        valid_wallet_tags = ["all", "pump_smart", "smart_degen", "reowned", "snipe_bot"]

        if timeframe not in valid_timeframes or wallet_tag not in valid_wallet_tags:
            raise ValueError("Invalid timeframe or wallet tag")

        params = {
            "tag": wallet_tag,
            "orderby": f"pnl_{timeframe}",
            "direction": order,
        }

        # Build the endpoint URL
        url = self.endpoint.get_url(self.endpoint.TRENDING_WALLETS, timeframe=timeframe)

        self.client.queue_request(url, params)

        # Make the request
        response = await self.client.execute_requests()

        return WalletsResponse.model_validate(response[0])

    async def get_token_info(self, contract_address: str) -> dict:
        if not contract_address:
            raise ValueError("Must provide a contract address")
        url = self.endpoint.get_url(self.endpoint.TOKEN_INFO, contract_address=contract_address)
        # Queue the request
        return self.client.queue_request(url)

    async def get_wallet_info(
            self,
            wallet_address: Union[str, List[str]],
            timeout: int = 0,
            period: str = "7d") -> List[Union[WalletInfoResponse, None]]:
        # todo: document that lists of wallets can now be sent to get_wallet_info
        # todo: document that returning it as a list will keep return type consistent. plugin developers don't need to worry about str or list, it will always be a list
        valid_periods = ["7d", "30d"]
        if not wallet_address:
            raise ValueError("Must provide a wallet address")
        if period not in valid_periods:
            raise ValueError(f"Invalid period: {period}")

        # convert wallet_address to list
        if isinstance(wallet_address, str):
            wallet_address = [wallet_address]

        params = {"period": period}
        # build the endpoint url
        # url = self.endpoint.get_url(self.endpoint.WALLET_INFO, wallet_address=wallet_address)

        # Easier
        for wallet in wallet_address:
            url = f"https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/{wallet}"
            # Append the request to later on parallelize it
            self.client.queue_request(url, params, timeout)

        return self._validate_wallet_info(
            await self.client.execute_requests()
        )

    def _validate_wallet_info(self, response: List[dict]) -> list:
        # todo add docstring
        # todo maybe switch to pandas for better data manipulation?
        results = []
        for r in response:
            if r:
                try:
                    validated = WalletInfoResponse.model_validate(r)
                    results.append(validated)
                except Exception as e:
                    # Log failure for this wallet.
                    self.client.logger.error(f"Validation failed for response: {r}, error: {e}")
                    results.append(None)
            else:
                results.append(None)
        return results


if __name__ == "__main__":
    pass
