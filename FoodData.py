import requests

# Define the API endpoint for products
api_url = 'https://world.openfoodfacts.org/api/v0/product/'

# Example product codes (you can add more or fetch dynamically)
product_codes = ['737628064502', '3017620429484', '5000159484695']

# Function to get product details
def get_product_details(product_code):
    response = requests.get(f'{api_url}{product_code}.json')
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data for product code: {product_code}')
        return None

# Fetch details for each product and extract allergens
for code in product_codes:
    product_data = get_product_details(code)
    if product_data:
        product_name = product_data.get('product', {}).get('product_name', 'Unknown')
        allergens = product_data.get('product', {}).get('allergens_tags', [])
        print(f'Product: {product_name}')
        print(f'Allergens: {", ".join(allergens) if allergens else "None"}')
        print('-' * 40)

