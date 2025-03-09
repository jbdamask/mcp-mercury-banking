# Mercury MCP Server

This is a simple MCP (Mercury Control Protocol) server that provides access to Mercury bank accounts through the Mercury API.

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install httpx python-dotenv mcp-sdk
   ```
3. Create a `.env` file in the root directory with your Mercury API key:
   ```
   MERCURY_API_KEY=your_mercury_api_key_here
   ```
   You can obtain an API key from the Mercury developer dashboard.

## Usage

### Running the server

Run the server with:

```bash
python mcp-mercury.py
```

### Available Resources

- `mercury://accounts` - Lists all Mercury bank accounts

### Available Tools

- `get_account_details(account_id)` - Get detailed information about a specific account

## Example Usage with MCP Client

```python
from mcp.client import Client

async def main():
    # Connect to the MCP server
    client = await Client.connect("mercury")
    
    # List all accounts
    accounts = await client.get_resource("mercury://accounts")
    print(f"Found {len(accounts)} accounts:")
    for account in accounts:
        print(f"- {account['name']} ({account['id']}): {account['balance']['amount']} {account['balance']['currency']}")
    
    # Get details for a specific account
    if accounts:
        account_id = accounts[0]["id"]
        details = await client.invoke_tool("get_account_details", {"account_id": account_id})
        print(f"\nDetails for account {account_id}:")
        print(details)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Security Note

This server requires your Mercury API key which has access to sensitive financial information. Never share your API key or commit it to version control.
