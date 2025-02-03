from WalletWave.models.wallets import WalletsResponse
from WalletWave.models.wallet_info import WalletInfoResponse
#from WalletWave.services.gmgn_client.client import Gmgn
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

    async def get_wallet_info(self, wallet_address: str, timeout: int = 0, period: str = "7d") -> WalletInfoResponse:
        valid_periods = ["7d", "30d"]
        if not wallet_address:
            raise ValueError("Must provide a wallet address")
        if period not in valid_periods:
            raise ValueError(f"Invalid period: {period}")

        params = {"period": period}
        # build the endpoint url
        #url = self.endpoint.get_url(self.endpoint.WALLET_INFO, wallet_address=wallet_address)
        
        # Easier 
        url = f"https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/{wallet_address}"
        
        # Append the request to later on parallelize it
        self.client.queue_request(url, params, timeout)
        response = await self.client.execute_requests()

        return WalletInfoResponse.model_validate(response[0])

if __name__ == "__main__":
    # repo = GmgnRepo()
    # test = repo.get_trending_wallets("7d", "smart_degen")2

    #
    # for wallet in test.rank:
    #     print(f"Address: {wallet.wallet_address}")
    pass