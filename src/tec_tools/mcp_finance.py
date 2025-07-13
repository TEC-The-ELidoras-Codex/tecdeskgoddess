"""
Finance MCP Server - The Wealth Codex
Part of TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion

This MCP server exposes financial tracking and cryptocurrency analysis functionality,
providing comprehensive financial tracking, expenditure patterns, and sophisticated
crypto insights augmented by AI capabilities.
"""

import json
import os
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .mcp_base import MCPServer
import logging

logger = logging.getLogger(__name__)

class FinanceMCPServer(MCPServer):
    """
    MCP Server for The Wealth Codex - Finance Tracker & Crypto Analysis
    """
    
    def __init__(self):
        super().__init__("wealth-codex-finance", "1.0.0")
        
        # API keys for external services
        self.coingecko_api_key = os.environ.get("COINGECKO_API_KEY")
        self.binance_api_key = os.environ.get("BINANCE_API_KEY")
        self.binance_secret = os.environ.get("BINANCE_SECRET")
        
        # Define capabilities
        self.capabilities = {
            "resources": {
                "crypto_prices": "Real-time cryptocurrency prices",
                "portfolio_data": "User cryptocurrency portfolio",
                "market_analysis": "AI-powered market analysis",
                "transaction_history": "Financial transaction history",
                "spending_patterns": "Analysis of spending patterns"
            },
            "tools": {
                "get_crypto_price": "Get current cryptocurrency prices",
                "analyze_portfolio": "Analyze cryptocurrency portfolio",
                "track_transaction": "Add financial transaction",
                "generate_market_summary": "Generate AI market summary",
                "calculate_portfolio_value": "Calculate total portfolio value",
                "get_spending_insights": "Get AI spending insights"
            },
            "prompts": {
                "investment_analysis": "Generate investment analysis prompts",
                "risk_assessment": "Generate risk assessment prompts",
                "financial_planning": "Generate financial planning prompts"
            }
        }
    
    def get_resources(self) -> List[Dict[str, Any]]:
        """Return available finance resources"""
        return [
            {
                "uri": "finance://crypto/prices",
                "name": "Cryptocurrency Prices",
                "description": "Real-time cryptocurrency prices and market data",
                "mimeType": "application/json"
            },
            {
                "uri": "finance://portfolio/overview",
                "name": "Portfolio Overview",
                "description": "User's cryptocurrency portfolio overview",
                "mimeType": "application/json"
            },
            {
                "uri": "finance://analysis/market",
                "name": "Market Analysis",
                "description": "AI-powered market analysis and insights",
                "mimeType": "application/json"
            },
            {
                "uri": "finance://transactions/recent",
                "name": "Recent Transactions",
                "description": "Recent financial transactions",
                "mimeType": "application/json"
            }
        ]
    
    def read_resource_data(self, uri: str) -> Dict[str, Any]:
        """Read finance resource data"""
        try:
            if uri == "finance://crypto/prices":
                return self._get_crypto_prices()
            elif uri == "finance://portfolio/overview":
                return self._get_portfolio_overview()
            elif uri == "finance://analysis/market":
                return self._get_market_analysis()
            elif uri == "finance://transactions/recent":
                return self._get_recent_transactions()
            else:
                return {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps({"error": f"Unknown resource: {uri}"})
                }
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return {
                "uri": uri,
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available finance tools"""
        return [
            {
                "name": "get_crypto_price",
                "description": "Get current cryptocurrency prices",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbols": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Cryptocurrency symbols (e.g., ['BTC', 'ETH', 'XRP'])"
                        },
                        "vs_currency": {
                            "type": "string",
                            "description": "Currency to compare against",
                            "default": "usd"
                        }
                    },
                    "required": ["symbols"]
                }
            },
            {
                "name": "analyze_portfolio",
                "description": "Analyze cryptocurrency portfolio performance",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {"type": "string", "description": "User ID"},
                        "analysis_type": {
                            "type": "string",
                            "description": "Type of analysis",
                            "enum": ["performance", "risk", "diversification", "recommendations"]
                        }
                    },
                    "required": ["userId"]
                }
            },
            {
                "name": "track_transaction",
                "description": "Add a financial transaction",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "userId": {"type": "string", "description": "User ID"},
                        "type": {"type": "string", "description": "Transaction type", "enum": ["income", "expense", "crypto_buy", "crypto_sell"]},
                        "amount": {"type": "number", "description": "Transaction amount"},
                        "currency": {"type": "string", "description": "Currency or crypto symbol"},
                        "category": {"type": "string", "description": "Transaction category"},
                        "description": {"type": "string", "description": "Transaction description"}
                    },
                    "required": ["userId", "type", "amount", "currency"]
                }
            },
            {
                "name": "generate_market_summary",
                "description": "Generate AI-powered market summary",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "timeframe": {
                            "type": "string",
                            "description": "Timeframe for analysis",
                            "enum": ["24h", "7d", "30d"],
                            "default": "24h"
                        },
                        "focus": {
                            "type": "string",
                            "description": "Focus area",
                            "enum": ["general", "crypto", "stocks", "defi"],
                            "default": "crypto"
                        }
                    }
                }
            }
        ]
    
    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute finance tools"""
        try:
            if name == "get_crypto_price":
                return self._get_crypto_price_tool(arguments)
            elif name == "analyze_portfolio":
                return self._analyze_portfolio_tool(arguments)
            elif name == "track_transaction":
                return self._track_transaction_tool(arguments)
            elif name == "generate_market_summary":
                return self._generate_market_summary_tool(arguments)
            else:
                return {
                    "type": "text",
                    "text": f"Unknown tool: {name}"
                }
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return {
                "type": "text",
                "text": f"Error executing {name}: {str(e)}"
            }
    
    def get_prompts(self) -> List[Dict[str, Any]]:
        """Return available finance prompts"""
        return [
            {
                "name": "investment_analysis",
                "description": "Generate investment analysis prompts",
                "arguments": [
                    {
                        "name": "asset",
                        "description": "Asset to analyze",
                        "required": True
                    },
                    {
                        "name": "timeframe",
                        "description": "Analysis timeframe",
                        "required": False
                    }
                ]
            },
            {
                "name": "risk_assessment",
                "description": "Generate risk assessment prompts",
                "arguments": [
                    {
                        "name": "portfolio_type",
                        "description": "Type of portfolio",
                        "required": False
                    }
                ]
            },
            {
                "name": "financial_planning",
                "description": "Generate financial planning prompts",
                "arguments": [
                    {
                        "name": "goal",
                        "description": "Financial goal",
                        "required": False
                    }
                ]
            }
        ]
    
    def get_prompt_data(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get finance prompt data"""
        try:
            if name == "investment_analysis":
                return self._get_investment_analysis_prompt(arguments)
            elif name == "risk_assessment":
                return self._get_risk_assessment_prompt(arguments)
            elif name == "financial_planning":
                return self._get_financial_planning_prompt(arguments)
            else:
                return {
                    "description": f"Unknown prompt: {name}",
                    "messages": []
                }
        except Exception as e:
            logger.error(f"Error getting prompt {name}: {e}")
            return {
                "description": f"Error getting prompt {name}: {str(e)}",
                "messages": []
            }
    
    def _get_crypto_prices(self) -> Dict[str, Any]:
        """Get current cryptocurrency prices"""
        try:
            # Mock data - replace with actual CoinGecko API call
            mock_prices = {
                "bitcoin": {
                    "symbol": "BTC",
                    "current_price": 45000.00,
                    "price_change_24h": 2.5,
                    "price_change_percentage_24h": 5.88,
                    "market_cap": 850000000000,
                    "volume_24h": 25000000000
                },
                "ethereum": {
                    "symbol": "ETH",
                    "current_price": 3200.00,
                    "price_change_24h": 85.50,
                    "price_change_percentage_24h": 2.75,
                    "market_cap": 385000000000,
                    "volume_24h": 15000000000
                },
                "ripple": {
                    "symbol": "XRP",
                    "current_price": 0.65,
                    "price_change_24h": 0.08,
                    "price_change_percentage_24h": 14.06,
                    "market_cap": 35000000000,
                    "volume_24h": 5000000000
                }
            }
            
            return {
                "uri": "finance://crypto/prices",
                "mimeType": "application/json",
                "text": json.dumps({
                    "prices": mock_prices,
                    "last_updated": datetime.now().isoformat(),
                    "source": "coingecko"
                })
            }
            
        except Exception as e:
            logger.error(f"Error getting crypto prices: {e}")
            return {
                "uri": "finance://crypto/prices",
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def _get_portfolio_overview(self) -> Dict[str, Any]:
        """Get portfolio overview"""
        try:
            # Mock portfolio data
            mock_portfolio = {
                "total_value_usd": 15750.00,
                "total_change_24h": 425.50,
                "total_change_percentage_24h": 2.78,
                "holdings": [
                    {
                        "symbol": "BTC",
                        "amount": 0.25,
                        "value_usd": 11250.00,
                        "percentage": 71.43,
                        "change_24h": 281.25
                    },
                    {
                        "symbol": "ETH",
                        "amount": 1.5,
                        "value_usd": 4800.00,
                        "percentage": 30.48,
                        "change_24h": 128.25
                    },
                    {
                        "symbol": "XRP",
                        "amount": 200,
                        "value_usd": 130.00,
                        "percentage": 0.83,
                        "change_24h": 16.00
                    }
                ]
            }
            
            return {
                "uri": "finance://portfolio/overview",
                "mimeType": "application/json",
                "text": json.dumps({
                    "portfolio": mock_portfolio,
                    "last_updated": datetime.now().isoformat()
                })
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio overview: {e}")
            return {
                "uri": "finance://portfolio/overview",
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def _get_market_analysis(self) -> Dict[str, Any]:
        """Get AI-powered market analysis"""
        try:
            # Mock market analysis
            mock_analysis = {
                "market_sentiment": "bullish",
                "key_insights": [
                    "Bitcoin showing strong support at $44,000 level",
                    "Ethereum maintaining momentum above $3,000",
                    "XRP experiencing significant volume spike following recent news",
                    "Overall market showing signs of institutional accumulation"
                ],
                "risk_factors": [
                    "Regulatory uncertainty in key markets",
                    "Potential macroeconomic headwinds",
                    "High volatility expected in short term"
                ],
                "recommendations": [
                    "Consider dollar-cost averaging for long-term positions",
                    "Monitor support levels for potential entry points",
                    "Diversify across different asset classes"
                ],
                "generated_at": datetime.now().isoformat()
            }
            
            return {
                "uri": "finance://analysis/market",
                "mimeType": "application/json",
                "text": json.dumps(mock_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error getting market analysis: {e}")
            return {
                "uri": "finance://analysis/market",
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def _get_recent_transactions(self) -> Dict[str, Any]:
        """Get recent financial transactions"""
        try:
            # Mock transaction data
            mock_transactions = [
                {
                    "id": "tx_1",
                    "type": "crypto_buy",
                    "amount": 0.05,
                    "currency": "BTC",
                    "value_usd": 2250.00,
                    "timestamp": datetime.now().isoformat(),
                    "category": "investment",
                    "description": "BTC purchase - DCA strategy"
                },
                {
                    "id": "tx_2",
                    "type": "expense",
                    "amount": 45.00,
                    "currency": "USD",
                    "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
                    "category": "food",
                    "description": "Grocery shopping"
                },
                {
                    "id": "tx_3",
                    "type": "income",
                    "amount": 3500.00,
                    "currency": "USD",
                    "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
                    "category": "salary",
                    "description": "Monthly salary"
                }
            ]
            
            return {
                "uri": "finance://transactions/recent",
                "mimeType": "application/json",
                "text": json.dumps({
                    "transactions": mock_transactions,
                    "total": len(mock_transactions),
                    "last_updated": datetime.now().isoformat()
                })
            }
            
        except Exception as e:
            logger.error(f"Error getting recent transactions: {e}")
            return {
                "uri": "finance://transactions/recent",
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)})
            }
    
    def _get_crypto_price_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Tool to get cryptocurrency prices"""
        try:
            symbols = arguments.get("symbols", [])
            vs_currency = arguments.get("vs_currency", "usd")
            
            if not symbols:
                return {
                    "type": "text",
                    "text": "Error: No symbols provided"
                }
            
            # Mock price data
            prices = {}
            for symbol in symbols:
                if symbol.upper() == "BTC":
                    prices[symbol] = {"price": 45000.00, "change_24h": 2.5}
                elif symbol.upper() == "ETH":
                    prices[symbol] = {"price": 3200.00, "change_24h": 2.75}
                elif symbol.upper() == "XRP":
                    prices[symbol] = {"price": 0.65, "change_24h": 14.06}
                else:
                    prices[symbol] = {"price": 0.00, "change_24h": 0.00}
            
            result = f"Current prices in {vs_currency.upper()}:\\n"
            for symbol, data in prices.items():
                result += f"{symbol.upper()}: ${data['price']:,.2f} ({data['change_24h']:+.2f}%)\\n"
            
            return {
                "type": "text",
                "text": result
            }
            
        except Exception as e:
            logger.error(f"Error getting crypto prices: {e}")
            return {
                "type": "text",
                "text": f"Error getting crypto prices: {str(e)}"
            }
    
    def _analyze_portfolio_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Tool to analyze portfolio"""
        try:
            user_id = arguments.get("userId")
            analysis_type = arguments.get("analysis_type", "performance")
            
            if not user_id:
                return {
                    "type": "text",
                    "text": "Error: userId is required"
                }
            
            # Mock analysis results
            analysis_results = {
                "performance": "Portfolio showing strong performance with 2.78% gain in 24h. BTC position contributing most to gains.",
                "risk": "Portfolio has moderate risk profile with 71% concentration in BTC. Consider diversification.",
                "diversification": "Portfolio is heavily weighted towards BTC (71%). Recommend increasing allocation to other assets.",
                "recommendations": "Consider taking profits on BTC position and increasing ETH allocation. Monitor XRP for potential opportunities."
            }
            
            result = analysis_results.get(analysis_type, "Unknown analysis type")
            
            return {
                "type": "text",
                "text": f"Portfolio Analysis ({analysis_type}): {result}"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio: {e}")
            return {
                "type": "text",
                "text": f"Error analyzing portfolio: {str(e)}"
            }
    
    def _track_transaction_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Tool to track financial transaction"""
        try:
            user_id = arguments.get("userId")
            transaction_type = arguments.get("type")
            amount = arguments.get("amount")
            currency = arguments.get("currency")
            category = arguments.get("category", "")
            description = arguments.get("description", "")
            
            if not all([user_id, transaction_type, amount, currency]):
                return {
                    "type": "text",
                    "text": "Error: userId, type, amount, and currency are required"
                }
            
            # Create transaction record
            transaction = {
                "userId": user_id,
                "type": transaction_type,
                "amount": amount,
                "currency": currency,
                "category": category,
                "description": description,
                "timestamp": datetime.now().isoformat()
            }
            
            # TODO: Save to database
            
            return {
                "type": "text",
                "text": f"Transaction recorded: {transaction_type} {amount} {currency} - {description}"
            }
            
        except Exception as e:
            logger.error(f"Error tracking transaction: {e}")
            return {
                "type": "text",
                "text": f"Error tracking transaction: {str(e)}"
            }
    
    def _generate_market_summary_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Tool to generate market summary"""
        try:
            timeframe = arguments.get("timeframe", "24h")
            focus = arguments.get("focus", "crypto")
            
            summaries = {
                "crypto": {
                    "24h": "Cryptocurrency markets showing bullish momentum with BTC leading gains at +2.5%. XRP experiencing significant volume spike with +14% surge. Overall market sentiment remains positive with institutional interest continuing.",
                    "7d": "Weekly crypto performance shows consolidation phase with BTC maintaining support above $44k. Altcoins showing mixed signals with some DeFi tokens gaining traction.",
                    "30d": "Monthly crypto trends indicate potential breakthrough above key resistance levels. Market maturity increasing with more institutional adoption."
                },
                "general": {
                    "24h": "Financial markets showing mixed performance with crypto leading gains. Traditional markets experiencing volatility due to macroeconomic factors.",
                    "7d": "Weekly market overview shows rotation from traditional assets to alternative investments including crypto and commodities.",
                    "30d": "Monthly financial landscape indicates shift towards digital assets and decentralized finance solutions."
                }
            }
            
            summary = summaries.get(focus, {}).get(timeframe, "Market data not available for specified parameters")
            
            return {
                "type": "text",
                "text": f"Market Summary ({timeframe} - {focus}): {summary}"
            }
            
        except Exception as e:
            logger.error(f"Error generating market summary: {e}")
            return {
                "type": "text",
                "text": f"Error generating market summary: {str(e)}"
            }
    
    def _get_investment_analysis_prompt(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get investment analysis prompt"""
        asset = arguments.get("asset", "cryptocurrency")
        timeframe = arguments.get("timeframe", "medium-term")
        
        prompt_text = f"Analyze the investment potential of {asset} for {timeframe} investment strategy. Consider market trends, technical indicators, fundamental analysis, and risk factors."
        
        return {
            "description": f"Investment analysis prompt for {asset}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        }
    
    def _get_risk_assessment_prompt(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get risk assessment prompt"""
        portfolio_type = arguments.get("portfolio_type", "diversified")
        
        prompt_text = f"Assess the risk profile of a {portfolio_type} portfolio. Evaluate volatility, correlation, potential downside scenarios, and risk mitigation strategies."
        
        return {
            "description": f"Risk assessment prompt for {portfolio_type} portfolio",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        }
    
    def _get_financial_planning_prompt(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get financial planning prompt"""
        goal = arguments.get("goal", "wealth building")
        
        prompt_text = f"Create a financial planning strategy for {goal}. Include asset allocation, timeline, risk management, and milestone tracking."
        
        return {
            "description": f"Financial planning prompt for {goal}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        }


if __name__ == "__main__":
    # Run the Finance MCP Server
    server = FinanceMCPServer()
    server.run(port=5002, debug=True)
