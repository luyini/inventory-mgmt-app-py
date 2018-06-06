import csv
import os

def menu(username="@prof-rossetti", products_count="100"):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product."""
    #Please select an operation: # end of multi- line string. also using string interpolation
    return menu

products = []

def read_products_from_file(filename="products.csv"):# First, read products from file...
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            #print(row["name"], row["price"])
            products.append(dict(row))
    #TODO: open the file and populate the products list with product dictionaries
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader() # uses fieldnames set above
        for p in products:
            writer.writerow(p)



def list_products():
    print("------------------------")
    print("LISTING  " + str(len(products)) + "  PRODUCTS:")
    print("------------------------")
    for product in products:
        print("+ Product #" + str(product["id"]) + ": " + product["name"])

def show_product():
    product_id = input("OK. Please specify the product's identifier:")
    product = [p for p in products if p["id"] == product_id]
    if product:
        print("--------------------------")
        print("SHOWING A PRODUCT: ")
        print("--------------------------")
        print(product)
    else:
        print("--------------------------")
        print("COULDN'T FIND A PRODUCT WITH IDENTIFIER", product)
        print("--------------------------")



headers = ["id", "name", "aisle", "department", "price"]
user_input_headers = [header for header in headers if header != "id"]

def get_product_id(product): return int(product["id"])

def auto_incremented_id():
    product_ids = map(get_product_id, products)
    return max(product_ids) + 1

def create_product():
    print("OK. PLEASE PROVIDE THE PRODUCT'S INFORMATION...")
    product = {"id": auto_incremented_id() }
    for header in user_input_headers:
        product[header] = input("OK. Please input the product's '{0}': ".format(header))
    products.append(product)
    print("--------------------------")
    print("CREATING A NEW PRODUCT: ")
    print("--------------------------")
    print(product)
    write_products_to_file(products=products)



def destroy_product():
    product_id = input("OK. Please specify the product's identifier: ")
    product = [p for p in products if p["id"] == product_id][0]
    if product:
        print("--------------------------")
        print("DESTROYING A PRODUCT HERE")
        print("--------------------------")
        print(product)
        del products[products.index(product)]
    else:
        print("COULDN'T FIND A PRODUCT WITH IDENTIFIER", product_id)
    write_products_to_file(products=products)


def update_product():
    product_id = input("OK. Please specify the product's identifier:")
    product = [p for p in products if p["id"] == product_id][0]
    if product:
        print("OK. PLEASE PROVIDE THE PRODUCT'S INFORMATION...")
        for header in user_input_headers:
            #product[header] = input("What is product's new '{0}' (currently:'{1}'): ".format(header, product[header]))
            product[hearder] = input(f"What is product's new {header} (currently: {product[header]}) : ")
        print("--------------------------")
        print("UPDATED A PRODUCT HERE")
        print("--------------------------")
        print(product)
    else:
        print("COULDN'T FIND A PRODUCT WITH IDENTIFIER", product_id)
    write_products_to_file(products=products)


def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

#def enlarge(my_number):
#    return my_number * 100



def run():

    products = read_products_from_file()

    # Then, prompt the user to select an operation...
    input_username = input("Please enter your username: ")#TODO instead of printing, capture user input
    print(menu(username = input_username, products_count=len(products)))


    operation = input("Please Select An Operation: ")
    print("YOU CHOSE:", operation)

    if operation.title() == "List":
        list_products()
    elif operation.title() == "Show":
        show_product()
    elif operation.title() == "Create":
        create_product()
    elif operation.title() == "Update":
        update_product()
    elif operation.title() == "Destroy":
        destroy_product()
    elif operation.title() == "Reset":
        reset_products_file()
    else:
        print("Unrecognized Operation. Please choose one of: 'List', 'Show', 'Create', 'Update', or 'Destroy'.")


    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    #TODO: handle selected operation

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)

# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
