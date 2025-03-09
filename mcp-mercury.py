from typing import Any, List, Dict, Optional
import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp import types
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp-server-mercury.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('mercury-mcp')
logger.info("Starting Mercury MCP server")

# Load environment variables from .env file
load_dotenv()

# Get MERCURY_API_KEY from environment variables
MERCURY_API_KEY = os.getenv("MERCURY_API_KEY")
if not MERCURY_API_KEY:
    raise ValueError("MERCURY_API_KEY environment variable is required")

# Initialize FastMCP server
mcp = FastMCP("mercury")

# Constants
API_BASE = "https://api.mercury.com/api/v1"
USER_AGENT = "mercury-app/1.0"

class MercuryClient:
    """Client for interacting with the Mercury API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            # "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    
    async def get_accounts(self) -> List[Dict[str, Any]]:
        """Get all accounts from Mercury API"""
        logger.info("Getting accounts from Mercury API")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE}/accounts",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            # Return the accounts list from the response
            return data.get("accounts", [])
            
    async def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get a specific account from Mercury API"""
        logger.info(f"Getting account {account_id} from Mercury API")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE}/account/{account_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
            
    async def get_cards(self, account_id: str) -> List[Dict[str, Any]]:
        """Get cards associated with a specific account from Mercury API"""
        logger.info(f"Getting cards for account {account_id} from Mercury API")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE}/account/{account_id}/cards",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            # Return the cards list from the response
            return data.get("cards", [])
            
    async def get_transactions(self, account_id: str, limit: int = 500, offset: int = 0, order: str = "desc") -> Dict[str, Any]:
        """Get transactions for a specific account from Mercury API"""
        logger.info(f"Getting transactions for account {account_id} from Mercury API")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE}/account/{account_id}/transactions?limit={limit}&offset={offset}&order={order}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
            
    async def get_transaction(self, account_id: str, transaction_id: str) -> Dict[str, Any]:
        """Get a specific transaction from Mercury API"""
        logger.info(f"Getting transaction {transaction_id} for account {account_id} from Mercury API")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE}/account/{account_id}/transaction/{transaction_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

# Initialize Mercury client
mercury_client = MercuryClient(MERCURY_API_KEY)

@mcp.tool()
async def list_accounts() -> str:
    """List all Mercury bank accounts"""
    accounts = await mercury_client.get_accounts()
    logger.info(f"Found {len(accounts)} accounts")  
    logger.info(f"Accounts: {accounts}")
    
    # Format accounts for better readability
    formatted_accounts = []
    for account in accounts:
        formatted_account = {
            "id": account.get("id"),
            "name": account.get("name"),
            "nickname": account.get("nickname"),
            "legalBusinessName": account.get("legalBusinessName"),
            "type": account.get("type"),
            "kind": account.get("kind"),
            "status": account.get("status"),
            "accountNumber": account.get("accountNumber"),
            "routingNumber": account.get("routingNumber"),
            "currentBalance": account.get("currentBalance"),
            "availableBalance": account.get("availableBalance"),
            "createdAt": account.get("createdAt"),
            "canReceiveTransactions": account.get("canReceiveTransactions"),
        }
        # Convert dictionary to a formatted string
        account_str = "\n".join([f"{key}: {value}" for key, value in formatted_account.items() if value is not None])
        formatted_accounts.append(account_str)
    
    return "\n---\n".join(formatted_accounts)

@mcp.tool()
async def get_account(account_id: str) -> str:
    """Get a specific Mercury bank account"""
    account = await mercury_client.get_account(account_id)
    logger.info(f"Found account: {account}")  
    
    # Format accounts for better readability
    formatted_account = {
        "id": account.get("id"),
        "name": account.get("name"),
        "nickname": account.get("nickname"),
        "legalBusinessName": account.get("legalBusinessName"),
        "type": account.get("type"),
        "kind": account.get("kind"),
        "status": account.get("status"),
        "accountNumber": account.get("accountNumber"),
        "routingNumber": account.get("routingNumber"),
        "currentBalance": account.get("currentBalance"),
        "availableBalance": account.get("availableBalance"),
        "createdAt": account.get("createdAt"),
        "canReceiveTransactions": account.get("canReceiveTransactions"),
    }
    # Convert dictionary to a formatted string
    account_str = "\n".join([f"{key}: {value}" for key, value in formatted_account.items() if value is not None])
    return account_str

@mcp.tool()
async def get_account_cards(account_id: str) -> str:
    """Get all cards associated with a specific Mercury bank account"""
    cards = await mercury_client.get_cards(account_id)
    logger.info(f"Found {len(cards)} cards for account {account_id}")
    
    if not cards:
        return "No cards found for this account."
    
    # Format cards for better readability
    formatted_cards = []
    for card in cards:
        formatted_card = {
            "cardId": card.get("cardId"),
            "createdAt": card.get("createdAt"),
            "lastFourDigits": card.get("lastFourDigits"),
            "nameOnCard": card.get("nameOnCard"),
            "network": card.get("network"),
            "status": card.get("status"),
            "physicalCardStatus": card.get("physicalCardStatus")
        }
        # Convert dictionary to a formatted string
        card_str = "\n".join([f"{key}: {value}" for key, value in formatted_card.items() if value is not None])
        formatted_cards.append(card_str)
    
    return "\n---\n".join(formatted_cards)

@mcp.tool()
async def get_account_transactions(account_id: str, limit: int = 500, offset: int = 0, order: str = "desc") -> str:
    """Get transactions for a specific Mercury bank account
    
    Args:
        account_id: The ID of the account to get transactions for
        limit: Maximum number of transactions to return (default: 500)
        offset: Number of transactions to skip (default: 0)
        order: Sort order, either "asc" or "desc" (default: "desc")
    """
    transactions_data = await mercury_client.get_transactions(account_id, limit, offset, order)
    total = transactions_data.get("total", 0)
    transactions = transactions_data.get("transactions", [])
    
    logger.info(f"Found {len(transactions)} transactions for account {account_id} (total: {total})")
    
    if not transactions:
        return "No transactions found for this account."
    
    # Format transactions for better readability
    formatted_transactions = []
    for transaction in transactions:
        # Extract the most important transaction details
        formatted_transaction = {
            "id": transaction.get("id"),
            "amount": transaction.get("amount"),
            "counterpartyName": transaction.get("counterpartyName"),
            "counterpartyNickname": transaction.get("counterpartyNickname"),
            "kind": transaction.get("kind"),
            "status": transaction.get("status"),
            "createdAt": transaction.get("createdAt"),
            "postedAt": transaction.get("postedAt"),
            "note": transaction.get("note"),
            "externalMemo": transaction.get("externalMemo"),
            "bankDescription": transaction.get("bankDescription"),
            "mercuryCategory": transaction.get("mercuryCategory"),
        }
        
        # Add attachment information if available
        attachments = transaction.get("attachments", [])
        if attachments:
            formatted_transaction["attachments"] = f"{len(attachments)} attachment(s)"
        
        # Convert dictionary to a formatted string
        transaction_str = "\n".join([f"{key}: {value}" for key, value in formatted_transaction.items() if value is not None])
        formatted_transactions.append(transaction_str)
    
    summary = f"Showing {len(transactions)} of {total} total transactions"
    return f"{summary}\n\n" + "\n---\n".join(formatted_transactions)

@mcp.tool()
async def get_transaction(account_id: str, transaction_id: str) -> str:
    """Get a specific transaction from a Mercury bank account
    
    Args:
        account_id: The ID of the account the transaction belongs to
        transaction_id: The ID of the transaction to retrieve
    """
    transaction = await mercury_client.get_transaction(account_id, transaction_id)
    logger.info(f"Found transaction: {transaction}")
    
    # Format transaction for better readability
    formatted_transaction = {
        "id": transaction.get("id"),
        "amount": transaction.get("amount"),
        "counterpartyId": transaction.get("counterpartyId"),
        "counterpartyName": transaction.get("counterpartyName"),
        "counterpartyNickname": transaction.get("counterpartyNickname"),
        "kind": transaction.get("kind"),
        "status": transaction.get("status"),
        "createdAt": transaction.get("createdAt"),
        "postedAt": transaction.get("postedAt"),
        "estimatedDeliveryDate": transaction.get("estimatedDeliveryDate"),
        "failedAt": transaction.get("failedAt"),
        "reasonForFailure": transaction.get("reasonForFailure"),
        "note": transaction.get("note"),
        "externalMemo": transaction.get("externalMemo"),
        "bankDescription": transaction.get("bankDescription"),
        "mercuryCategory": transaction.get("mercuryCategory"),
        "generalLedgerCodeName": transaction.get("generalLedgerCodeName"),
        "compliantWithReceiptPolicy": transaction.get("compliantWithReceiptPolicy"),
        "hasGeneratedReceipt": transaction.get("hasGeneratedReceipt"),
        "dashboardLink": transaction.get("dashboardLink"),
    }
    
    # Add details information if available
    details = transaction.get("details")
    if details:
        if details.get("debitCardInfo"):
            formatted_transaction["debitCardInfo"] = details.get("debitCardInfo")
        if details.get("creditCardInfo"):
            formatted_transaction["creditCardInfo"] = details.get("creditCardInfo")
    
    # Add currency exchange information if available
    currency_exchange = transaction.get("currencyExchangeInfo")
    if currency_exchange:
        formatted_transaction["currencyExchangeInfo"] = {
            "convertedFromCurrency": currency_exchange.get("convertedFromCurrency"),
            "convertedToCurrency": currency_exchange.get("convertedToCurrency"),
            "convertedFromAmount": currency_exchange.get("convertedFromAmount"),
            "convertedToAmount": currency_exchange.get("convertedToAmount"),
            "exchangeRate": currency_exchange.get("exchangeRate"),
        }
    
    # Add attachment information if available
    attachments = transaction.get("attachments", [])
    if attachments:
        attachment_info = []
        for attachment in attachments:
            attachment_info.append(f"{attachment.get('fileName')} ({attachment.get('attachmentType')}): {attachment.get('url')}")
        formatted_transaction["attachments"] = "\n".join(attachment_info)
    
    # Convert dictionary to a formatted string
    transaction_str = "\n".join([f"{key}: {value}" for key, value in formatted_transaction.items() if value is not None])
    return transaction_str

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
# # Run the server when this script is executed directly
# if __name__ == "__main__":
#     import asyncio
#     from mcp.server.stdio import stdio_server
    
#     async def main():
#         async with stdio_server() as streams:
#             await mcp.run(
#                 streams[0],
#                 streams[1],
#                 mcp.create_initialization_options()
#             )
    
#     asyncio.run(main())
