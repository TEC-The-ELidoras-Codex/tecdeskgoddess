"""
TEC Crypto API Manager - CoinGecko Alternatives
Multi-provider crypto data with fallback logic following TEC philosophy
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

class TECCryptoManager:
    """
    Multi-provider crypto data manager with fallback logic
    Supports free and premium APIs as CoinGecko alternatives
    """
    
    def __init__(self):
        self.providers = {
            "coinmarketcap": {
                "api_key": os.environ.get("COINMARKETCAP_API_KEY"),
                "base_url": "https://pro-api.coinmarketcap.com/v1",
                "free_limit": 10000,  # calls/month
                "rate_limit": 30,     # calls/minute
            },
            "cryptocompare": {
                "api_key": os.environ.get("CRYPTOCOMPARE_API_KEY"),
                "base_url": "https://min-api.cryptocompare.com/data",
                "free_limit": 250000,  # calls/month
                "rate_limit": 100,     # calls/second
            },
            "binance": {
                "api_key": os.environ.get("BINANCE_API_KEY"),
                "secret": os.environ.get("BINANCE_SECRET_KEY"),
                "base_url": "https://api.binance.com/api/v3",
                "free_limit": "unlimited",
                "rate_limit": 1200,   # requests/minute
            },
            "kraken": {
                "api_key": os.environ.get("KRAKEN_API_KEY"),
                "secret": os.environ.get("KRAKEN_SECRET_KEY"),
                "base_url": "https://api.kraken.com/0/public",
                "free_limit": "unlimited",
                "rate_limit": 1,      # call/second for public
            },
            "coinbase": {
                "api_key": os.environ.get("COINBASE_API_KEY"),
                "base_url": "https://api.coinbase.com/v2",
                "free_limit": 10000,  # calls/hour
                "rate_limit": 10000,  # calls/hour
            }
        }
        
        # Fallback order (free first, most reliable)
        self.fallback_order = ["cryptocompare", "binance", "kraken", "coinmarketcap", "coinbase"]
        
    def get_price(self, symbol: str, vs_currency: str = "usd") -> Optional[Dict]:
        """Get current price with fallback logic"""
        
        for provider in self.fallback_order:
            try:
                if not self._has_credentials(provider):
                    continue
                    
                result = self._get_price_from_provider(provider, symbol, vs_currency)
                if result:
                    result["provider"] = provider
                    result["timestamp"] = datetime.now().isoformat()
                    return result
                    
            except Exception as e:
                print(f"❌ {provider} failed: {e}")
                continue
                
        return None
    
    def get_portfolio_value(self, holdings: Dict[str, float]) -> Dict:
        """Calculate total portfolio value"""
        
        portfolio = {
            "total_value": 0,
            "holdings": {},
            "updated": datetime.now().isoformat(),
            "provider": None
        }
        
        for symbol, amount in holdings.items():
            price_data = self.get_price(symbol)
            if price_data:
                value = price_data["price"] * amount
                portfolio["holdings"][symbol] = {
                    "amount": amount,
                    "price": price_data["price"],
                    "value": value,
                    "change_24h": price_data.get("change_24h", 0)
                }
                portfolio["total_value"] += value
                portfolio["provider"] = price_data["provider"]
            else:
                portfolio["holdings"][symbol] = {
                    "amount": amount,
                    "price": None,
                    "value": 0,
                    "error": "Price unavailable"
                }
        
        return portfolio
    
    def get_market_overview(self) -> Dict:
        """Get crypto market overview"""
        
        major_cryptos = ["bitcoin", "ethereum", "binancecoin", "cardano", "solana"]
        overview = {
            "top_cryptos": {},
            "market_summary": {},
            "updated": datetime.now().isoformat()
        }
        
        for crypto in major_cryptos:
            price_data = self.get_price(crypto)
            if price_data:
                overview["top_cryptos"][crypto] = price_data
        
        return overview
    
    def _has_credentials(self, provider: str) -> bool:
        """Check if provider has necessary credentials"""
        config = self.providers.get(provider, {})
        
        if provider in ["binance", "kraken"]:
            return bool(config.get("api_key"))  # Secret optional for public endpoints
        else:
            return bool(config.get("api_key"))
    
    def _get_price_from_provider(self, provider: str, symbol: str, vs_currency: str) -> Optional[Dict]:
        """Get price from specific provider"""
        
        if provider == "cryptocompare":
            return self._cryptocompare_price(symbol, vs_currency)
        elif provider == "binance":
            return self._binance_price(symbol, vs_currency)
        elif provider == "kraken":
            return self._kraken_price(symbol, vs_currency)
        elif provider == "coinmarketcap":
            return self._coinmarketcap_price(symbol, vs_currency)
        elif provider == "coinbase":
            return self._coinbase_price(symbol, vs_currency)
        
        return None
    
    def _cryptocompare_price(self, symbol: str, vs_currency: str) -> Optional[Dict]:
        """CryptoCompare API - 250k calls/month free"""
        try:
            url = f"{self.providers['cryptocompare']['base_url']}/price"
            params = {
                "fsym": symbol.upper(),
                "tsyms": vs_currency.upper()
            }
            
            if self.providers['cryptocompare']['api_key']:
                params["api_key"] = self.providers['cryptocompare']['api_key']
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = data.get(vs_currency.upper())
            
            if price:
                return {
                    "symbol": symbol,
                    "price": price,
                    "currency": vs_currency,
                    "provider": "cryptocompare"
                }
            
        except Exception as e:
            raise Exception(f"CryptoCompare error: {e}")
        
        return None
    
    def _binance_price(self, symbol: str, vs_currency: str) -> Optional[Dict]:
        """Binance API - Free with rate limits"""
        try:
            # Convert symbol format (bitcoin -> BTCUSDT)
            symbol_map = {
                "bitcoin": "BTCUSDT",
                "ethereum": "ETHUSDT",
                "binancecoin": "BNBUSDT",
                "cardano": "ADAUSDT",
                "solana": "SOLUSDT"
            }
            
            trading_pair = symbol_map.get(symbol.lower(), f"{symbol.upper()}USDT")
            
            url = f"{self.providers['binance']['base_url']}/ticker/price"
            params = {"symbol": trading_pair}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = float(data.get("price", 0))
            
            if price > 0:
                return {
                    "symbol": symbol,
                    "price": price,
                    "currency": vs_currency,
                    "provider": "binance"
                }
            
        except Exception as e:
            raise Exception(f"Binance error: {e}")
        
        return None
    
    def _kraken_price(self, symbol: str, vs_currency: str) -> Optional[Dict]:
        """Kraken API - Free public data"""
        try:
            # Convert symbol format
            symbol_map = {
                "bitcoin": "XXBTZUSD",
                "ethereum": "XETHZUSD",
                "cardano": "ADAUSD",
                "solana": "SOLUSD"
            }
            
            trading_pair = symbol_map.get(symbol.lower(), f"X{symbol.upper()}ZUSD")
            
            url = f"{self.providers['kraken']['base_url']}/Ticker"
            params = {"pair": trading_pair}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("error"):
                raise Exception(f"Kraken API error: {data['error']}")
            
            result = data.get("result", {})
            pair_data = result.get(trading_pair) or result.get(list(result.keys())[0] if result else "")
            
            if pair_data and "c" in pair_data:
                price = float(pair_data["c"][0])  # Last trade price
                return {
                    "symbol": symbol,
                    "price": price,
                    "currency": vs_currency,
                    "provider": "kraken"
                }
            
        except Exception as e:
            raise Exception(f"Kraken error: {e}")
        
        return None
    
    def _coinmarketcap_price(self, symbol: str, vs_currency: str) -> Optional[Dict]:
        """CoinMarketCap API - 10k calls/month free"""
        if not self.providers['coinmarketcap']['api_key']:
            return None
            
        try:
            url = f"{self.providers['coinmarketcap']['base_url']}/cryptocurrency/quotes/latest"
            headers = {
                "X-CMC_PRO_API_KEY": self.providers['coinmarketcap']['api_key']
            }
            params = {
                "symbol": symbol.upper(),
                "convert": vs_currency.upper()
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status", {}).get("error_code") == 0:
                crypto_data = data["data"][symbol.upper()]
                quote = crypto_data["quote"][vs_currency.upper()]
                
                return {
                    "symbol": symbol,
                    "price": quote["price"],
                    "currency": vs_currency,
                    "change_24h": quote.get("percent_change_24h", 0),
                    "market_cap": quote.get("market_cap"),
                    "provider": "coinmarketcap"
                }
            
        except Exception as e:
            raise Exception(f"CoinMarketCap error: {e}")
        
        return None
    
    def _coinbase_price(self, symbol: str, vs_currency: str) -> Optional[Dict]:
        """Coinbase API - 10k calls/hour free"""
        try:
            # Coinbase uses different symbol format
            symbol_map = {
                "bitcoin": "BTC",
                "ethereum": "ETH",
                "binancecoin": "BNB",
                "cardano": "ADA",
                "solana": "SOL"
            }
            
            coin_symbol = symbol_map.get(symbol.lower(), symbol.upper())
            
            url = f"{self.providers['coinbase']['base_url']}/exchange-rates"
            params = {"currency": coin_symbol}
            
            if self.providers['coinbase']['api_key']:
                headers = {"Authorization": f"Bearer {self.providers['coinbase']['api_key']}"}
            else:
                headers = {}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get("data", {}).get("rates", {})
            price = float(rates.get(vs_currency.upper(), 0))
            
            if price > 0:
                return {
                    "symbol": symbol,
                    "price": price,
                    "currency": vs_currency,
                    "provider": "coinbase"
                }
            
        except Exception as e:
            raise Exception(f"Coinbase error: {e}")
        
        return None

# Example usage and testing
if __name__ == "__main__":
    crypto_manager = TECCryptoManager()
    
    print("🪙 Testing TEC Crypto Manager (CoinGecko Alternatives)")
    print("=" * 60)
    
    # Test individual price
    btc_price = crypto_manager.get_price("bitcoin")
    if btc_price:
        print(f"✅ Bitcoin: ${btc_price['price']:,.2f} (via {btc_price['provider']})")
    else:
        print("❌ Bitcoin price unavailable")
    
    # Test portfolio
    sample_portfolio = {
        "bitcoin": 0.1,
        "ethereum": 2.0,
        "solana": 10.0
    }
    
    portfolio_value = crypto_manager.get_portfolio_value(sample_portfolio)
    print(f"\n💼 Portfolio Value: ${portfolio_value['total_value']:,.2f}")
    
    for symbol, data in portfolio_value['holdings'].items():
        if 'error' not in data:
            print(f"   {symbol}: {data['amount']} @ ${data['price']:,.2f} = ${data['value']:,.2f}")
    
    print(f"\n🎯 TEC Crypto Manager ready - Multiple providers available!")
