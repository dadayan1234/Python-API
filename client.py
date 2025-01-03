import requests
from prettytable import PrettyTable

API_URL = "http://127.0.0.1:8000/items"

def print_items(data):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Description", "Price"]
    for item in data:
        table.add_row([item["id"], item["name"], item["description"], item["price"]])
    print(table)

# Test API
def test_api():
    # Create an item
    print("Creating an item...")
    payload = {"name": "Laptop", "description": "A high-performance laptop", "price": 1500.0}
    response = requests.post(API_URL, json=payload)
    print(response.json())

    # Read all items
    print("\nReading all items...")
    response = requests.get(API_URL)
    print_items(response.json())

    # Update an item
    print("\nUpdating the first item...")
    first_item = response.json()[0]
    update_payload = {"name": "Updated Laptop", "description": "Updated description", "price": 1400.0}
    update_response = requests.put(f"{API_URL}/{first_item['id']}", json=update_payload)
    print(update_response.json())

    # Read specific item
    print("\nReading the updated item...")
    response = requests.get(f"{API_URL}/{first_item['id']}")
    print(response.json())

    # Delete an item
    print("\nDeleting the first item...")
    delete_response = requests.delete(f"{API_URL}/{first_item['id']}")
    print(delete_response.json())

    # Confirm deletion
    print("\nReading all items after deletion...")
    response = requests.get(API_URL)
    print_items(response.json())

if __name__ == "__main__":
    test_api()
