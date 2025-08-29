from agents import Agent, Runner, function_tool,trace
from connection import config
import requests
import rich

# 🛠️ Tool to fetch and filter products
@function_tool
def search_products(query: str, max_price: float = None) -> list:
    """
    Searches products by keyword and optional price limit.
    """
    url = "https://next-ecommerce-template-4.vercel.app/api/product"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
    except Exception as e:
        return [{
            "title": "Error fetching products",
            "price": "N/A",
            "description": str(e),
            "image": "",
            "link": ""
        }]

    # Filter based on query and price
    results = []
    for p in products:
        name = p.get("name", "").lower()
        price = float(p.get("price", 0))

        if query.lower() in name and (max_price is None or price <= max_price):
            results.append({
                "title": p.get("name", "Unnamed"),
                "price": f"${price}",
                "description": p.get("description", ""),
                "image": p.get("imagePath", ""),
                "category": p.get("category", "Unknown"),
                "discount": f"{p.get('discountPercentage', 0)}%",
            })

    return results[:5] if results else [{
        "title": f"No '{query}' found under ${max_price}",
        "price": "N/A",
        "description": "Try a different search or increase your price range.",
        "image": "",
        "category": "",
        "discount": ""
    }]

# 🤖 Shopping Agent setup
agent = Agent(
    name="shopping-agent",
    instructions="You are a smart shopping assistant. Use tools to help users find affordable products by name and price.",
    tools=[search_products],
)

# 🧪 Test the agent
prompt = "Find me a chair under 500 dollars"
result = Runner.run_sync(
        agent, 
        prompt, 
        run_config=config
        )

# 📤 Output the result
rich.print("\n User Prompt: ",prompt)
rich.print("\nFinal Output:\n", result.final_output)
