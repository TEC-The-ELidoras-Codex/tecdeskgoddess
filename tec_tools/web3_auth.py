#!/usr/bin/env python3
"""
Web3 Authentication Module for TEC: BITLyfe
Handles multi-chain wallet authentication with Azure integration
"""
import os
import json
import jwt
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from web3 import Web3
from eth_account.messages import encode_defunct
import logging

logger = logging.getLogger(__name__)

class Web3AuthManager:
    """Manages Web3 authentication across multiple chains"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.jwt_secret = os.getenv('JWT_SECRET', 'your-super-secret-key-change-this')
        self.jwt_expiry = 24 * 60 * 60  # 24 hours
        
        # Initialize Web3 instances for supported chains
        self.web3_instances = {
            'ethereum': None,
            'polygon': None,
            'binance': None
        }
        
        # Chain configurations
        self.chain_configs = {
            'ethereum': {
                'name': 'Ethereum',
                'chain_id': 1,
                'rpc_url': os.getenv('ETH_RPC_URL', 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID')
            },
            'polygon': {
                'name': 'Polygon',
                'chain_id': 137,
                'rpc_url': os.getenv('POLYGON_RPC_URL', 'https://polygon-mainnet.infura.io/v3/YOUR_PROJECT_ID')
            },
            'binance': {
                'name': 'Binance Smart Chain',
                'chain_id': 56,
                'rpc_url': os.getenv('BSC_RPC_URL', 'https://bsc-dataseed.binance.org/')
            }
        }
        
        # Initialize Web3 connections
        self._init_web3_connections()
        
        # Supported wallet types
        self.supported_wallets = {
            'metamask': {'chains': ['ethereum', 'polygon', 'binance']},
            'walletconnect': {'chains': ['ethereum', 'polygon', 'binance']},
            'coinbase': {'chains': ['ethereum', 'polygon']},
            'trust': {'chains': ['ethereum', 'polygon', 'binance']}
        }
    
    def _init_web3_connections(self):
        """Initialize Web3 connections for supported chains"""
        for chain_name, chain_config in self.chain_configs.items():
            try:
                if chain_config['rpc_url'] and 'YOUR_PROJECT_ID' not in chain_config['rpc_url']:
                    self.web3_instances[chain_name] = Web3(Web3.HTTPProvider(chain_config['rpc_url']))
                    logger.info(f"Connected to {chain_name} network")
                else:
                    logger.warning(f"No RPC URL configured for {chain_name}")
            except Exception as e:
                logger.error(f"Failed to connect to {chain_name}: {e}")
    
    def generate_nonce(self, wallet_address: str) -> str:
        """Generate a unique nonce for wallet authentication"""
        timestamp = str(int(time.time()))
        data = f"{wallet_address}:{timestamp}:{self.jwt_secret}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def create_sign_message(self, wallet_address: str, nonce: str) -> str:
        """Create a message for wallet signing"""
        message = f"""Welcome to TEC: BITLyfe - The Creator's Rebellion!

By signing this message, you're entering the Astradigital Ocean and confirming your identity.

Wallet: {wallet_address}
Nonce: {nonce}
Time: {datetime.now().isoformat()}

This request will not trigger any blockchain transaction or cost any fees.
"""
        return message
    
    def verify_ethereum_signature(self, message: str, signature: str, wallet_address: str) -> bool:
        """Verify Ethereum/EVM signature"""
        try:
            # Get the appropriate Web3 instance (try ethereum first)
            web3 = self.web3_instances.get('ethereum')
            if not web3:
                logger.error("No Ethereum Web3 instance available")
                return False
            
            # Encode the message
            message_encoded = encode_defunct(text=message)
            
            # Recover the address from signature
            recovered_address = web3.eth.account.recover_message(message_encoded, signature=signature)
            
            # Compare addresses (case-insensitive)
            return recovered_address.lower() == wallet_address.lower()
            
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    def verify_signature(self, chain: str, message: str, signature: str, wallet_address: str) -> bool:
        """Verify signature for different chains"""
        if chain in ['ethereum', 'polygon', 'binance']:
            return self.verify_ethereum_signature(message, signature, wallet_address)
        # Add other chain verification methods here
        else:
            logger.error(f"Unsupported chain: {chain}")
            return False
    
    def generate_jwt_token(self, wallet_address: str, chain: str, user_data: Dict[str, Any]) -> str:
        """Generate JWT token for authenticated user"""
        payload = {
            'wallet_address': wallet_address,
            'chain': chain,
            'user_id': user_data.get('user_id'),
            'access_tier': user_data.get('access_tier', 'free'),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expiry)
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("JWT token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.error("Invalid JWT token")
            return None
    
    def authenticate_wallet(self, wallet_address: str, signature: str, message: str, chain: str) -> Dict[str, Any]:
        """Main authentication method"""
        try:
            # Verify the signature
            if not self.verify_signature(chain, message, signature, wallet_address):
                return {'success': False, 'error': 'Invalid signature'}
            
            # Here you would typically check your user database
            # For now, we'll create a basic user profile
            user_data = {
                'user_id': f"user_{wallet_address[:8]}",
                'wallet_address': wallet_address,
                'chain': chain,
                'access_tier': 'free',  # Default tier
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat()
            }
            
            # Generate JWT token
            token = self.generate_jwt_token(wallet_address, chain, user_data)
            
            return {
                'success': True,
                'token': token,
                'user_data': user_data,
                'message': 'Authentication successful'
            }
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {'success': False, 'error': 'Authentication failed'}

class TokenGateManager:
    """Manages token-gated access and subscription tiers"""
    
    def __init__(self, web3_auth: Web3AuthManager):
        self.web3_auth = web3_auth
        
        # Define access tiers and requirements
        self.access_tiers = {
            'free': {
                'name': 'Free Tier',
                'features': ['basic_chat', 'simple_journal'],
                'limits': {'messages_per_day': 100}
            },
            'alpha': {
                'name': 'Alpha Tier',
                'features': ['advanced_chat', 'journal', 'finance', 'quests'],
                'limits': {'messages_per_day': 1000},
                'requirements': {'nft_collections': ['MetaSteed'], 'min_bitl_balance': 0}
            },
            'beta': {
                'name': 'Beta Tier',
                'features': ['all_features', 'voice_synthesis', 'advanced_ai'],
                'limits': {'messages_per_day': 5000},
                'requirements': {'nft_collections': ['MetaSteed', 'Glitchwitch'], 'min_bitl_balance': 1000}
            },
            'creator': {
                'name': 'Creator Tier',
                'features': ['unlimited_access', 'api_access', 'custom_models'],
                'limits': {'messages_per_day': -1},  # Unlimited
                'requirements': {'nft_collections': ['MetaSteed', 'Glitchwitch'], 'min_bitl_balance': 10000}
            }
        }
        
        # NFT contract addresses (placeholder - replace with actual addresses)
        self.nft_contracts = {
            'MetaSteed': {
                'ethereum': '0x1234567890123456789012345678901234567890',
                'polygon': '0x1234567890123456789012345678901234567890'
            },
            'Glitchwitch': {
                'ethereum': '0x0987654321098765432109876543210987654321',
                'polygon': '0x0987654321098765432109876543210987654321'
            }
        }
        
        # BITL token addresses (placeholder)
        self.bitl_contracts = {
            'ethereum': '0xBITL000000000000000000000000000000000000',
            'polygon': '0xBITL000000000000000000000000000000000000'
        }
    
    def check_nft_ownership(self, wallet_address: str, chain: str, collection: str) -> bool:
        """Check if wallet owns NFTs from specified collection"""
        try:
            web3 = self.web3_auth.web3_instances.get(chain)
            if not web3:
                logger.error(f"No Web3 instance for chain: {chain}")
                return False
            
            contract_address = self.nft_contracts.get(collection, {}).get(chain)
            if not contract_address:
                logger.error(f"No contract address for {collection} on {chain}")
                return False
            
            # Basic ERC-721 ABI for balanceOf
            abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                }
            ]
            
            contract = web3.eth.contract(address=contract_address, abi=abi)
            balance = contract.functions.balanceOf(wallet_address).call()
            
            return balance > 0
            
        except Exception as e:
            logger.error(f"Error checking NFT ownership: {e}")
            return False
    
    def check_bitl_balance(self, wallet_address: str, chain: str) -> int:
        """Check BITL token balance"""
        try:
            web3 = self.web3_auth.web3_instances.get(chain)
            if not web3:
                return 0
            
            contract_address = self.bitl_contracts.get(chain)
            if not contract_address:
                return 0
            
            # Basic ERC-20 ABI for balanceOf
            abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "account", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                }
            ]
            
            contract = web3.eth.contract(address=contract_address, abi=abi)
            balance = contract.functions.balanceOf(wallet_address).call()
            
            # Convert from wei to tokens (assuming 18 decimals)
            return balance // (10 ** 18)
            
        except Exception as e:
            logger.error(f"Error checking BITL balance: {e}")
            return 0
    
    def determine_access_tier(self, wallet_address: str, chain: str) -> str:
        """Determine user's access tier based on holdings"""
        try:
            # Check from highest tier to lowest
            for tier_name in ['creator', 'beta', 'alpha']:
                tier_config = self.access_tiers[tier_name]
                requirements = tier_config.get('requirements', {})
                
                # Check NFT requirements
                nft_requirement_met = True
                for collection in requirements.get('nft_collections', []):
                    if not self.check_nft_ownership(wallet_address, chain, collection):
                        nft_requirement_met = False
                        break
                
                # Check BITL balance requirement
                min_bitl = requirements.get('min_bitl_balance', 0)
                bitl_balance = self.check_bitl_balance(wallet_address, chain)
                bitl_requirement_met = bitl_balance >= min_bitl
                
                # If all requirements met, return this tier
                if nft_requirement_met and bitl_requirement_met:
                    return tier_name
            
            # Default to free tier
            return 'free'
            
        except Exception as e:
            logger.error(f"Error determining access tier: {e}")
            return 'free'
