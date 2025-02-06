from enum import Enum

class GmgnEndpoints(Enum):
    BASE_URL = "https://gmgn.ai/defi/quotation"
    TOKEN_INFO = "/v1/tokens/sol/{contract_address}"
    TRENDING_WALLETS = "/v1/rank/sol/wallets/{timeframe}"
    WALLET_INFO = "/v1/smartmoney/sol/walletNew/{wallet_address}"

    @staticmethod
    def _token_info(contract_address: str) -> str:
        """
        Constructs the URL for the TOKEN_INFO endpoint.

        Args:
            contract_address (str): The contract address for the token.

        Returns:
            str: The full URL for the TOKEN_INFO endpoint.
        """
        return f"{GmgnEndpoints.BASE_URL.value}{GmgnEndpoints.TOKEN_INFO.value.format(contract_address=contract_address)}"

    @staticmethod
    def _trending_wallets(timeframe: str) -> str:
        """
        Constructs the URL for the Trending Wallets endpoint

        Args:
            timeframe (str): Timeframe to search for trending wallets (1d, 7d, 30d)

        Returns:
            str: The full URL for the TRENDING_WALLETS endpoint
        """
        return f"{GmgnEndpoints.BASE_URL.value}{GmgnEndpoints.TRENDING_WALLETS.value.format(timeframe=timeframe)}"

    @staticmethod
    def _wallet_info(wallet_address: str) -> str:
        """
        Constructs the URL for the WALLET_INFO endpoint

        Args:
            wallet_address (str): Address of SOLANA wallet

        Returns:
            str: The full URL for the WALLET_INFO endpoint
        """
        return f"{GmgnEndpoints.BASE_URL.value}{GmgnEndpoints.WALLET_INFO.value.format(wallet_address=wallet_address)}"

    @classmethod
    def get_url(cls, endpoint: "GmgnEndpoints", **kwargs) -> str:
        """
        Constructs the URL for the given endpoint dynamically.

        Args:
            endpoint (GmgnEndpoints): The endpoint Enum value.
            **kwargs: Parameters required for constructing the endpoint URL.

        Returns:
            str: The full URL.

        Raises:
            ValueError: If the endpoint is not supported or required parameters are missing.
        """
        # Map endpoint types to their respective static methods
        endpoint_methods = {
            cls.TOKEN_INFO: cls._token_info,
            cls.TRENDING_WALLETS: cls._trending_wallets,
            cls.WALLET_INFO: cls._wallet_info,
        }

        # Check if the endpoint is supported
        if endpoint not in endpoint_methods:
            raise ValueError(f"Unsupported endpoint: {endpoint}")

        # Call the corresponding method dynamically
        method = endpoint_methods[endpoint]
        return method(**kwargs)
