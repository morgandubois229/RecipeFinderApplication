import psycopg2

def create_connection():
    recipefinderconnection = psycopg2.connect(database="recipefinder", user="postgres",
                                              password="cat123",host="127.0.0.1", port="5432")
    recipefinderconnection.autocommit = True

    return recipefinderconnection

def close_connection(current_connection):
    current_connection.close()

def random_command(databasecursor): #test command
    databasecursor.execute("SELECT ID, name, Barcode  from Ingredient;")
    rows = databasecursor.fetchall()
    for row in rows:
        print("ID = ", row[0])
        print("NAME = ", row[1])
        print("Barcode = ", row[2])

def check_account(databasecursor, the_email, the_password): #check if email is in database
    command = "SELECT email, password FROM Customer WHERE email = %s AND password = %s;"
    databasecursor.execute(command, (the_email, the_password,))
    rows = databasecursor.fetchall()
    if(len(rows) == 0):
        return 0
    else:
        return 1

"""
currentConnection = create_connection()
check_account(currentConnection.cursor(), "Testuserperson@email.com", "Password")
close_connection(currentConnection)
"""
def check_email(databasecursor, the_email): #check if email is in database
    command = "SELECT email FROM Customer WHERE email LIKE %s;"
    databasecursor.execute(command, (the_email,))
    rows = databasecursor.fetchall()
    if(len(rows) == 0):
        return 0
    else:
        return 1

def create_account(databasecursor, the_email, the_password, first_name, middle_name, last_name): #create a customer account

    if(len(middle_name) == 0):
        command = "INSERT INTO Customer (Firstname, Middlename, Lastname, email, password) Values (%s, NULL, %s, %s, %s);"
        databasecursor.execute(command, (first_name, last_name, the_email, the_password))
    else:
        command = "INSERT INTO Customer (Firstname, Middlename, Lastname, email, password) Values (%s, %s, %s, %s, %s);"
        databasecursor.execute(command, (first_name, middle_name, last_name, the_email, the_password))


def check_selected_store(databasecursor, the_email): #checks if customer already has a selected store
    command = "SELECT StoreID FROM Customer WHERE Customer.email = %s AND customer.storeID IS NOT NULL"
    databasecursor.execute(command, (the_email,))
    rows = databasecursor.fetchall()
    if len(rows) == 1:
        return 1
    else:
        return 0

def return_selected_store(databasecursor, the_email):
    command = "SELECT StoreID FROM Customer WHERE Customer.email = %s"
    databasecursor.execute(command, (the_email,))
    rows = databasecursor.fetchall()
    return rows #returns the storeid a customer has saved using their email

def check_zipcode(databasecursor, the_zipcode):
    command = "SELECT StoreNumber, Street, City, State, Zipcode FROM Store WHERE Store.Zipcode = %s"
    databasecursor.execute(command, (the_zipcode,))
    rows = databasecursor.fetchall()
    return rows #returns information on a store based on zipcode input

def return_selected_store_info(databasecursor, the_store_number):
    command = "SELECT StoreNumber, Street, City, State, Zipcode FROM Store WHERE Store.StoreNumber = %s"
    databasecursor.execute(command, (the_store_number,))
    rows = databasecursor.fetchall()
    return rows #returns the info of the store with the store number input

def return_selected_store_info_fromID(databasecursor, the_store_id):
    command = "SELECT StoreNumber, Street, City, State, Zipcode FROM Store WHERE Store.ID = %s"
    databasecursor.execute(command, (the_store_id,))
    rows = databasecursor.fetchall()
    return rows #returns the info of the store with the store number input

def get_store_id(databasecursor, the_store_number):#gets store id based on store number
    command = "SELECT ID FROM Store WHERE StoreNumber = %s"
    databasecursor.execute(command, (the_store_number,))
    rows = databasecursor.fetchall()
    return rows[0][0]

def select_store(databasecursor, the_store_number, the_email): #updates the customer to have a store id
    the_store_number = get_store_id(databasecursor, the_store_number)
    command = "UPDATE Customer set StoreID = %s WHERE Customer.email = %s"
    databasecursor.execute(command, (the_store_number, the_email,))

def check_store(databasecursor, the_store_number): #checks if store with input store number is in the database
    command = "SELECT StoreNumber FROM Store WHERE Store.StoreNumber = %s"
    databasecursor.execute(command, (the_store_number,))
    rows = databasecursor.fetchall()
    if len(rows) == 0:
        return 0
    else:
        return 1

def get_customer_id(databasecursor, the_email): #gets customerid based on their email
    command = "SELECT ID FROM Customer WHERE email = %s"
    databasecursor.execute(command, (the_email,))
    rows = databasecursor.fetchall()
    return rows[0][0]

def get_ingredient_id(databasecursor, the_barcode): #gets ingredientid based on their barcode
    command = "SELECT ID FROM Ingredient WHERE barcode = %s"
    databasecursor.execute(command, (the_barcode,))
    rows = databasecursor.fetchall()
    return rows[0][0]

def select_ingredient(databasecursor, the_email, the_barcode): #updates the chosen ingredients to have an entry
    the_customer_id = get_customer_id(databasecursor, the_email)
    the_ingredient_id = get_ingredient_id(databasecursor, the_barcode)
    command = "INSERT INTO ChosenIngredients (CustomerID, IngredientID) VALUES (%s, %s);"
    databasecursor.execute(command, (the_customer_id, the_ingredient_id,))

def select_recipe(databasecursor, the_email, the_recipe_number): #updates the chosen recipes to have an entry
    the_customer_id = get_customer_id(databasecursor, the_email)
    the_recipe_id = get_recipe_id(databasecursor, the_recipe_number)
    if(the_recipe_id == -1):
        return -1
    command = "INSERT INTO ChosenRecipes (CustomerID, RecipeID) VALUES (%s, %s);"
    databasecursor.execute(command, (the_customer_id, the_recipe_id,))

def check_ingredient(databasecursor, the_ingredient_name):
    command = "SELECT name, barcode FROM Ingredient WHERE LOWER(Ingredient.name) LIKE LOWER(%s)"
    databasecursor.execute(command, (the_ingredient_name,))
    rows = databasecursor.fetchall()
    return rows #returns information on an ingredient based on barcode input

def check_barcode(databasecursor, the_barcode): #checks if barcode is in db
    command = "SELECT barcode FROM Ingredient WHERE Ingredient.barcode = %s"
    databasecursor.execute(command, (the_barcode,))
    rows = databasecursor.fetchall()
    if len(rows) == 0:
        return 0
    else:
        return 1

def get_recipe_id(databasecursor, the_recipe_num): #gets recipeid based on their num
    if(len(the_recipe_num) == 0):
        return -1
    command = "SELECT ID FROM Recipe WHERE recipenumber = %s"
    databasecursor.execute(command, (the_recipe_num,))
    rows = databasecursor.fetchall()
    if(len(rows) == 0):
        return -1
    return rows[0][0]

def check_recipe(databasecursor, the_recipe_name):
    command = "SELECT name, recipenumber FROM Recipe WHERE LOWER(Recipe.name) LIKE LOWER(%s)"
    databasecursor.execute(command, (the_recipe_name,))
    rows = databasecursor.fetchall()
    return rows #returns information on a recipe based on recipenumber input

def check_recipe_number(databasecursor, the_recipe_num): #checks if recipenum is in db
    command = "SELECT recipenumber FROM Recipe WHERE recipenumber = %s"
    check_validity = get_recipe_id(databasecursor, the_recipe_num)
    if(check_validity == -1):
        return 0
    databasecursor.execute(command, (the_recipe_num,))
    rows = databasecursor.fetchall()
    if len(rows) == 0:
        return 0
    else:
        return 1

def get_recipe_info(databasecursor, the_recipe_num):
    command = "SELECT name, recipenumber, description FROM Recipe WHERE recipenumber = %s"
    databasecursor.execute(command, (the_recipe_num,))
    rows = databasecursor.fetchall()
    return rows #returns information on a recipe based on recipenumber input, includes desc

def remove_ingredient(databasecursor, the_email, the_barcode): #updates the chosen ingredients to remove an entry
    the_customer_id = get_customer_id(databasecursor, the_email)
    the_ingredient_id = get_ingredient_id(databasecursor, the_barcode)
    command = "DELETE FROM ChosenIngredients WHERE CustomerID = %s AND IngredientID = %s;"
    databasecursor.execute(command, (the_customer_id, the_ingredient_id,))

def remove_recipe(databasecursor, the_email, the_recipe_num): #updates the chosen recipes to remove an entry
    the_customer_id = get_customer_id(databasecursor, the_email)
    the_recipe_id = get_recipe_id(databasecursor, the_recipe_num)
    if(the_recipe_id == -1):
        return;
    command = "DELETE FROM ChosenRecipes WHERE CustomerID = %s AND RecipeID = %s;"
    databasecursor.execute(command, (the_customer_id, the_recipe_id,))

def check_barcode_choseningredient(databasecursor, the_barcode, the_email): #checks if barcode is in choseningr
    the_ingredient_id = get_ingredient_id(databasecursor, the_barcode)
    the_customer_id = get_customer_id(databasecursor, the_email)
    command = "SELECT Ingredientid FROM ChosenIngredients WHERE IngredientID = %s AND CustomerID = %s"
    databasecursor.execute(command, (the_ingredient_id,the_customer_id,))
    rows = databasecursor.fetchall()
    if len(rows) == 0:
        return 0
    else:
        return 1

def check_recipenum_choseningredient(databasecursor, the_recipe_num, the_email): #checks if recipenum is in chosenrec
    the_recipe_id = get_recipe_id(databasecursor, the_recipe_num)
    the_customer_id = get_customer_id(databasecursor, the_email)
    if(the_recipe_id == -1):
        return;
    command = "SELECT RecipeID FROM ChosenRecipes WHERE RecipeID = %s AND CustomerID = %s"
    databasecursor.execute(command, (the_recipe_id,the_customer_id))
    rows = databasecursor.fetchall()
    print(rows)
    if len(rows) == 0:
        return 0
    else:
        return 1

def get_chosen_ingredients(databasecursor, the_email):
    the_customer_id = get_customer_id(databasecursor, the_email)
    command = "SELECT Ingredient.name, Ingredient.barcode \
              FROM Ingredient \
                JOIN ChosenIngredients ON (Ingredient.ID = ChosenIngredients.IngredientID) \
              WHERE ChosenIngredients.CustomerID = %s"
    databasecursor.execute(command, (the_customer_id,))
    rows = databasecursor.fetchall()
    return rows #returns table for chosen ingredients

def get_chosen_recipes(databasecursor, the_email):
    the_customer_id = get_customer_id(databasecursor, the_email)
    command = "SELECT Recipe.name, Recipe.recipenumber \
                FROM Recipe  \
                    JOIN ChosenRecipes ON (Recipe.ID = ChosenRecipes.RecipeID)  \
                WHERE ChosenRecipes.CustomerID = %s"
    databasecursor.execute(command, (the_customer_id,))
    rows = databasecursor.fetchall()
    return rows #returns table for chosen recipes

def search_recipes_with_ingredients(databasecursor, the_email, the_name): #search for recipes using ingredients in choseningredients table
    the_customer_id = get_customer_id(databasecursor, the_email)
    command = "SELECT DISTINCT recipe.name, recipe.recipenumber \
                FROM Recipe \
                    JOIN RecipeIngredients ON (recipe.ID = RecipeIngredients.Recipeid) \
                    JOIN ChosenIngredients ON (RecipeIngredients.IngredientID = ChosenIngredients.IngredientID) \
                WHERE ChosenIngredients.CustomerID = %s AND LOWER(Recipe.name) LIKE LOWER(%s)"
    databasecursor.execute(command, (the_customer_id, the_name,))
    rows = databasecursor.fetchall()
    return rows #returns table for recipes based on chosen ingredients

def check_choseningredients(databasecursor, the_email):
    cusID = get_customer_id(databasecursor, the_email)
    command = "SELECT COUNT(CustomerID) FROM ChosenIngredients WHERE CustomerID = %s"
    databasecursor.execute(command, (cusID,))
    returnVal = databasecursor.fetchall()
    print(returnVal)
    return returnVal[0][0]

def get_recipe_stock_info(databasecursor, the_email): #returns a bunch of info or something...
    the_customer_id = get_customer_id(databasecursor, the_email)
    the_store_id = return_selected_store(databasecursor, the_email)
    command = "SELECT DISTINCT barcode, Ingredient.name, price, InStock, aisle \
               FROM Ingredient \
                    JOIN Stock ON (ingredient.id = stock.ingredientid) \
                    JOIN recipeIngredients ON (ingredient.id = RecipeIngredients.ingredientid) \
                    JOIN Recipe ON (Recipe.id = RecipeIngredients.Recipeid) \
                    JOIN ChosenRecipes ON (Recipe.id = ChosenRecipes.Recipeid) \
               WHERE ChosenRecipes.CustomerID = %s AND Stock.StoreID = %s"
    databasecursor.execute(command, (the_customer_id, the_store_id[0][0],))
    rows = databasecursor.fetchall()
    return rows

def get_recipe_amounts(databasecursor,the_recipe_num):
    the_recipe_id = get_recipe_id(databasecursor, the_recipe_num)
    command = "SELECT Ingredient.name, amount, unit \
               FROM RecipeIngredients \
                    JOIN Ingredient ON (Ingredient.ID = recipeIngredients.ingredientid) \
               WHERE RecipeIngredients.RecipeID = %s"
    databasecursor.execute(command, (the_recipe_id,))
    rows = databasecursor.fetchall()
    return rows
