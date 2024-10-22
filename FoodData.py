import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to get a list of products in a given category
def get_products_by_category(category):
    # Define the URL for the category endpoint
    url = f"https://world.openfoodfacts.org/category/{category}.json"
    
    # Define headers to mimic a regular browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        # Make the GET request to the API with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the list of products
        products = data.get('products', [])
        
        # Create a list to store the product names and Nutri-Scores
        product_list = []
        
        # Loop through the products and extract relevant information
        for product in products:
            product_list.append({
                'Product Name': product.get('product_name', 'N/A'),
                'Nutri-Score': product.get('nutriscore_grade', 'N/A')
            })
        
        return product_list
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return []

# Function to plot Nutri-Score distribution with different colors
def plot_nutriscore_distribution(category):
    # Get the list of products in the given category
    products = get_products_by_category(category)
    
    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(products)
    
    # Filter out products without a Nutri-Score
    df = df[df['Nutri-Score'] != 'N/A']
    
    # Define colors for each Nutri-Score grade
    colors = {
        'a': 'green',
        'b': 'lightgreen',
        'c': 'yellow',
        'd': 'orange',
        'e': 'red'
    }
    
    # Plot the data with different colors for each Nutri-Score grade
    plt.figure(figsize=(12, 8))
    df['Nutri-Score'].value_counts().sort_index().plot(kind='bar', color=[colors[score] for score in df['Nutri-Score'].value_counts().sort_index().index])
    plt.xlabel('Nutri-Score')
    plt.ylabel('Number of Products')
    plt.title(f'Nutri-Score Distribution of {category.replace("-", " ").title()}')
    plt.show()

# List of specific categories to choose from
categories = [
    {"id": "meats-and-their-products", "name": "Meats and their products"},
    {"id": "plant-based-foods", "name": "Plant-based foods"},
    {"id": "snacks", "name": "Snacks"},
    {"id": "fruits", "name": "Fruits"},
    {"id": "cereals-and-their-products", "name": "Cereals and their products"}
]

while True:
    # Display 5 options of categories to choose from
    print("Choose a category from the following options:")
    for i, category in enumerate(categories):
        print(f"{i + 1}. {category['name']}")

    # Ask for a category choice from the user
    choice = input("Enter the number corresponding to your choice or type 'Done' to finish: ")
    
    if choice.lower() == 'done':
        print("Finished.")
        break
    
    try:
        choice = int(choice) - 1
        if choice < 0 or choice >= len(categories):
            raise ValueError("Invalid choice")
        
        # Get the selected category ID
        selected_category_id = categories[choice]['id']
        
        # Plot the Nutri-Score distribution for the selected category
        plot_nutriscore_distribution(selected_category_id)
    
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid number or type 'Done' to finish.")

