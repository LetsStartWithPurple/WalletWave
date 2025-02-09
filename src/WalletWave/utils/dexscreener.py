import requests as r
from typing import Optional, List, Dict
from pydantic import ValidationError
from WalletWave.utils.logging_utils import get_logger
from WalletWave.api.models.dexscreener.token_info import DexscreenerPairResponse

# Todo: Maybe add future chain integrations like Ethereum, Base, Abstract, etc..

class DexScreener:
    """
    Initialize the DexScreener class
    """
    def __init__(self, chain: str):
        self.chain = chain
        self.logger = get_logger("DexScreener API")

    async def get_token_info_by_address(self, token_address: str) -> Optional[List[Dict]]:
        self.logger.debug(f"Got token address {token_address}")
        self.logger.debug(f"Getting Token Pool Address for token {token_address}")
        try:
            response = r.get(
                f"https://api.dexscreener.com/token-pairs/v1/solana/{token_address}",
                headers={},
            )
            data = response.json()

            if not isinstance(data, list) or not data:
                self.logger.warning(f"No valid data received for token {token_address}")
                return None

            validated_data = {"data": data}

            # Validate the response to be DexscreenerPairResponse
            try:
                validated_response = DexscreenerPairResponse.model_validate(validated_data)
            except ValidationError as ve:
                self.logger.error(f"Validation error: {ve}")
                return None

            # Return all the possible token data (just in case) from which the interesting attributes can be taken
            token_data = [
                {
                    "chainId": pair.chainId,
                    "dexId": pair.dexId,
                    "url": pair.url,
                    "pairAddress": pair.pairAddress,
                    "labels": pair.labels if hasattr(pair, "labels") else [],  # Some tokens do not have "labels"
                    "baseToken": {
                        "address": pair.baseToken.address,
                        "name": pair.baseToken.name,
                        "symbol": pair.baseToken.symbol,
                    },
                    "quoteToken": {
                        "address": pair.quoteToken.address,
                        "name": pair.quoteToken.name,
                        "symbol": pair.quoteToken.symbol,
                    },
                    "priceNative": pair.priceNative,
                    "priceUsd": pair.priceUsd,
                    "txns": pair.txns,
                    "volume": pair.volume,
                    "priceChange": pair.priceChange,
                    "liquidity": {
                        # Todo: Investigate why some tokens return 0 in all the fields despite not being 0...
                        #       Example: 644MryX1MXBNjA8QEUNeQ5HSEVZZqGRzPdiLz4EBpump
                        "usd": pair.liquidity.usd if hasattr(pair.liquidity, "usd") else 0,
                        "base": pair.liquidity.base if hasattr(pair.liquidity, "base") else 0,
                        "quote": pair.liquidity.quote if hasattr(pair.liquidity, "quote") else 0,
                    },
                    "fdv": pair.fdv,
                    "marketCap": pair.marketCap,
                    "pairCreatedAt": pair.pairCreatedAt,
                    "info": {
                        "imageUrl": pair.info.imageUrl if hasattr(pair.info, "imageUrl") else None,
                        "header": pair.info.header if hasattr(pair.info, "header") else None,
                        "openGraph": pair.info.openGraph if hasattr(pair.info, "openGraph") else None,
                        "websites": [
                            {"label": getattr(site, "label", "unknown"), "url": site.url} for site in pair.info.websites
                            ] if hasattr(pair.info, "websites") else [],
                        "socials": [
                            {
                                "platform": getattr(social, "platform", "unknown"),
                                "handle": getattr(social, "handle", "unknown"),
                                "url": getattr(social, "url", None)
                            }
                            for social in pair.info.socials
                        ] if hasattr(pair.info, "socials") else [],
                    },
                }
                for pair in validated_response.data
            ]

            return token_data

        except Exception as e:
            self.logger.critical(f"Error while fetching {token_address} pool: {e}")
            return None
