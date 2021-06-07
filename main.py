# Imports
from tkinter import *
import SQLCommands

##################################################
# Main Window Code
##################################################

root = Tk()
root.title("Recipe Finder")
root.geometry('500x600')
instruction_label = Label(root, text='Current Instructions')
currentConnection = SQLCommands.create_connection()
current_email = ""


##################################################
# Re-Usable Functions
##################################################


def exit_application():
    root.destroy()
    SQLCommands.close_connection(currentConnection)
    exit()


def clear_screen():
    for i in root.grid_slaves():
        i.grid_remove()


def return_to_login():
    go_to_login()


def return_to_main_menu():
    go_to_main_menu()


def return_to_store():
    go_to_store()


def return_to_ingredient():
    go_to_ingredient()


def return_to_stock():
    go_to_stock()


def return_to_recipe():
    go_to_recipe()


def return_to_info():
    go_to_info()


##################################################
# Main Menu
##################################################
def go_to_main_menu():
    clear_screen()
    instruction_label.configure(text="Main Menu: Please select an option")
    instruction_label.grid(row=0, column=0)
    main_menu_quit_button.grid(row=2, column=1)
    main_menu_store_button.grid(row=2, column=0)
    main_menu_ingredient_button.grid(row=1, column=0)
    main_menu_stock_button.grid(row=1, column=1)


main_menu_quit_button = Button(root, text="Logut", command=return_to_login)
main_menu_store_button = Button(root, text="Change Store", command=return_to_store)
main_menu_ingredient_button = Button(root, text="Select Ingredients", command=return_to_ingredient)
main_menu_stock_button = Button(root, text="Stock", command=return_to_stock)

##################################################
# Create Account
##################################################


def go_to_create_account():
    clear_screen()
    first_name_entry.delete(0, 'end')
    middle_name_entry.delete(0, 'end')
    last_name_entry.delete(0, 'end')
    new_email_entry.delete(0, 'end')
    new_password_entry.delete(0, 'end')

    instruction_label.configure(text="Please fill in text boxes to create account." +
                                     " All boxes with a * are required")
    instruction_label.grid(row=0, column=0, columnspan=2)

    first_name_label.grid(row=1, column=0)
    middle_name_label.grid(row=2, column=0)
    last_name_label.grid(row=3, column=0)
    new_email_label.grid(row=4, column=0)
    new_password_label.grid(row=5, column=0)

    first_name_entry.grid(row=1, column=1)
    middle_name_entry.grid(row=2, column=1)
    last_name_entry.grid(row=3, column=1)
    new_email_entry.grid(row=4, column=1)
    new_password_entry.grid(row=5, column=1)

    create_account_button.grid(row=6, column=1)
    cancel_create_account_button.grid(row=6, column=0)


def try_create_account():
    global currentConnection
    first_name_input = first_name_entry.get()
    middle_name_input = middle_name_entry.get()
    last_name_input = last_name_entry.get()
    new_email_input = new_email_entry.get()
    new_password_input = new_password_entry.get()

    if (first_name_input == "" or last_name_input == "" or
            new_email_input == "" or new_password_input == ""):
        instruction_label.configure(text="Please fill out all required text boxes (*)")
    elif(len(first_name_input) > 15 or len(last_name_input) > 15 or len(middle_name_input) > 20 or
            len(new_email_input) > 40 or len(new_password_input) > 10):
        instruction_label.configure(text="Text entry too long. Please user a shorter entry")
        if(len(first_name_input) > 15):
            first_name_entry.delete(0, 'end')
        if(len(middle_name_input) > 15):
            middle_name_entry.delete(0, 'end')
        if(len(last_name_input) > 20):
            last_name_entry.delete(0, 'end')
        if(len(new_email_input) > 40):
            new_email_entry.delete(0,'end')
        if(len(new_password_input) > 10):
            new_password_entry.delete(0, 'end')
    elif (SQLCommands.check_email(currentConnection.cursor(), new_email_input)):
        instruction_label.configure(text="Email already in use, please try another one")
        new_email_entry.delete(0, 'end')
    else:
        SQLCommands.create_account(currentConnection.cursor(), new_email_input, new_password_input,
                                   first_name_input, middle_name_input, last_name_input)
        go_to_login()


first_name_input = ""
middle_name_input = ""
last_name_input = ""
new_email_input = ""
new_password_input = ""

first_name_label = Label(root, text="*First name:")
middle_name_label = Label(root, text="Middle name:")
last_name_label = Label(root, text="*Last name:")
new_email_label = Label(root, text="*Email:")
new_password_label = Label(root, text="*Password:")

first_name_entry = Entry(root, textvariable=first_name_label)
middle_name_entry = Entry(root, textvariable=middle_name_label)
last_name_entry = Entry(root, textvariable=last_name_label)
new_email_entry = Entry(root, textvariable=new_email_label)
new_password_entry = Entry(root, textvariable=new_password_label, show="*")

create_account_button = Button(root, text="Create Account", command=try_create_account)
cancel_create_account_button = Button(root, text="Cancel", command=return_to_login)


##################################################
# Choose/Change Store
##################################################
def go_to_store():
    global current_email
    global currentConnection
    clear_screen()
    user_zip_add_text.delete("1.0", 'end')
    user_zip_search_text.delete("1.0", "end")
    user_zip_add_entry.delete(0, 'end')
    user_zip_search_entry.delete(0, 'end')
    instruction_label.configure(text="Search for stores by zipcode and select one by inputting its number")
    instruction_label.grid(row=0, column=0, columnspan=2)

    user_zip_search_label.grid(row=1, column=0)
    user_zip_search_entry.grid(row=1, column=1)
    user_zip_search_button.grid(row=1, column=2)
    user_zip_search_text.grid(row=2, column=0)

    user_zip_add_label.grid(row=3, column=0)
    user_zip_add_entry.grid(row=3, column=1)
    user_zip_add_button.grid(row=3, column=2)
    user_zip_add_text.grid(row=4, column=0)

    if(SQLCommands.check_selected_store(currentConnection.cursor(), current_email) == 1):
        the_store = SQLCommands.return_selected_store(currentConnection.cursor(), current_email)
        store_info = SQLCommands.return_selected_store_info_fromID(currentConnection.cursor(), the_store[0][0])
        string_store_info = "Store Number: %s\n%s\n%s, %s\n%s\n\n" % (store_info[0][0], store_info[0][1], store_info[0][2], store_info[0][3], store_info[0][4])
        user_zip_add_text.insert(END, string_store_info)
        store_to_main_menu_button.grid(row=5, column=0)

    else:
        user_zip_add_text.insert(END, "No store has been selected")


def search_stores():
    global currentConnection
    user_zip_search_text.delete('1.0', 'end')
    user_zip_search_input = user_zip_search_entry.get()
    if(len(user_zip_search_input) == 0):
        user_zip_search_text.insert(END, "No stores found, please try again")
        return;
    found_stores = SQLCommands.check_zipcode(currentConnection.cursor(), user_zip_search_input)
    if(len(found_stores) == 0):
        user_zip_search_text.insert(END, "No stores found, please try again")
    else:
        for i in range(len(found_stores)):
            outputText = "Store Number: %s\n%s\n%s, %s\n%s\n\n" % (found_stores[i][0], found_stores[i][1], found_stores[i][2], found_stores[i][3], found_stores[i][4])
            user_zip_search_text.insert(END, outputText)


def add_store():
    global currentConnection
    global current_email
    user_zip_add_text.delete("1.0", "end")

    user_zip_add_input = user_zip_add_entry.get()
    if(SQLCommands.check_store(currentConnection.cursor(), user_zip_add_input)):
        SQLCommands.select_store(currentConnection.cursor(), user_zip_add_input, current_email)
        store_info = SQLCommands.return_selected_store_info(currentConnection.cursor(), user_zip_add_input)
        string_store_info = "Store Number: %s\n%s\n%s, %s\n%s\n\n" % (store_info[0][0], store_info[0][1], store_info[0][2], store_info[0][3], store_info[0][4])
        user_zip_add_text.insert(END, string_store_info)
        store_to_main_menu_button.grid(row=5, column=0)

    else:
        user_zip_add_text.insert(END, "Invalid store number")


user_zip_search_input = ""
user_zip_add_input = ""

user_zip_search_label = Label(root, text="Search for store by zipcode:")
user_zip_add_label = Label(root, text="Add store to profile with store number:")

user_zip_search_entry = Entry(root, textvariable=user_zip_search_input)
user_zip_add_entry = Entry(root, textvariable=user_zip_add_input)

user_zip_search_text = Text(root, height=10, width=35)
user_zip_add_text = Text(root, height=5, width=35)

user_zip_search_button = Button(root, text="Search", command=search_stores)
user_zip_add_button = Button(root, text="Add", command=add_store)

store_to_main_menu_button = Button(root, text='Main Menu', command=return_to_main_menu)

##################################################
# Choose/Change Ingredient
##################################################


def go_to_ingredient():
    global currentConnection
    global current_email

    ingredient_search_entry.delete(0, 'end')
    ingredient_remove_entry.delete(0, 'end')
    ingredient_add_entry.delete(0, 'end')
    ingredient_search_text.delete("1.0", "end")
    ingredient_add_remove_text.delete("1.0", "end")

    clear_screen()
    instruction_label.configure(text="Select Ingredients to narrow your recipe search with")
    instruction_label.grid(row=0, column=0)

    ingredient_search_label.grid(row=1, column=0)
    ingredient_search_entry.grid(row=2, column=0, sticky=W)
    ingredient_search_button.grid(row=2, column=0, sticky=E)
    ingredient_search_text.grid(row=3, column=0)

    ingredient_add_remove_label.grid(row=4, column=0)
    ingredient_add_entry.grid(row=5, column=0, sticky=W)
    ingredient_add_button.grid(row=5, column=0, sticky=E)
    ingredient_remove_entry.grid(row=6, column=0, sticky=W)
    ingredient_remove_button.grid(row=6, column=0, sticky=E)
    ingredient_add_remove_text.grid(row=7, column=0)

    to_recipe_selection_button.grid(row=7, column=1, sticky=S)

    saved_items = SQLCommands.get_chosen_ingredients(currentConnection.cursor(), current_email)
    for row in saved_items:
        output = "Name: %s\nBarcode: %s\n\n" % (row[0], row[1])
        ingredient_add_remove_text.insert(END, output)


def search_ingredient():
    global currentConnection
    global current_email

    ingredient_search_text.delete("1.0", "end")
    ingredient_search_input = ingredient_search_entry.get()
    ingredient_search_input = "%" + ingredient_search_input + "%"

    returned_items = SQLCommands.check_ingredient(currentConnection.cursor(), ingredient_search_input)
    for row in returned_items:
        output = "Name: %s\nBarcode: %s\n\n" % (row[0], row[1])
        ingredient_search_text.insert(END, output)

def add_ingredient():
    global currentConnection
    global current_email

    ingredient_add_remove_text.delete("1.0", "end")

    ingredient_add_input = ingredient_add_entry.get()
    if(SQLCommands.check_barcode(currentConnection.cursor(), ingredient_add_input)):
        if(SQLCommands.check_barcode_choseningredient(currentConnection.cursor(), ingredient_add_input, current_email) == 0):
            SQLCommands.select_ingredient(currentConnection.cursor(), current_email, ingredient_add_input)

    saved_items = SQLCommands.get_chosen_ingredients(currentConnection.cursor(), current_email)
    for row in saved_items:
        output = "Name: %s\nBarcode: %s\n\n" % (row[0], row[1])
        ingredient_add_remove_text.insert(END, output)


def remove_ingredient():
    global currentConnection
    global current_email

    ingredient_add_remove_text.delete("1.0", "end")
    ingredient_remove_input = ingredient_remove_entry.get()
    if(SQLCommands.check_barcode_choseningredient(currentConnection.cursor(), ingredient_remove_input, current_email)):
        SQLCommands.remove_ingredient(currentConnection.cursor(), current_email, ingredient_remove_input)

    saved_items = SQLCommands.get_chosen_ingredients(currentConnection.cursor(), current_email)
    for row in saved_items:
        output = "Name: %s\nBarcode: %s\n\n" % (row[0], row[1])
        ingredient_add_remove_text.insert(END, output)



ingredient_search_input = ""
ingredient_add_input = ""
ingredient_remove_input = ""

ingredient_search_label = Label(root, text="Search for an ingredient by its name")
ingredient_add_remove_label = Label(root, text="Add or Remove an ingredient using the barcode")

ingredient_search_text = Text(root, height=10, width=35)
ingredient_add_remove_text = Text(root, height=10, width=35)

ingredient_search_entry = Entry(root, textvariable=ingredient_search_input)
ingredient_add_entry = Entry(root, textvariable=ingredient_add_input)
ingredient_remove_entry = Entry(root, textvariable=ingredient_remove_input)

ingredient_search_button = Button(root, text="Search", command=search_ingredient)
ingredient_add_button = Button(root, text="Add", command=add_ingredient)
ingredient_remove_button = Button(root, text="Remove", command=remove_ingredient)

to_recipe_selection_button = Button(root, text="To Recipes", command=return_to_recipe)


##################################################
# Choose/Change Recipe
##################################################


def go_to_recipe():
    global currentConnection
    global current_email

    recipe_search_entry.delete(0, 'end')
    recipe_remove_entry.delete(0, 'end')
    recipe_add_entry.delete(0, 'end')
    recipe_search_text.delete("1.0", "end")
    recipe_add_remove_text.delete("1.0", "end")
    recipe_info_entry.delete(0, 'end')
    recipe_info_input = ""

    clear_screen()
    instruction_label.configure(text="Select recipes to narrow your recipe search with")
    instruction_label.grid(row=0, column=0)

    recipe_search_label.grid(row=1, column=0)
    recipe_search_entry.grid(row=2, column=0, sticky=W)
    recipe_search_button.grid(row=2, column=0, sticky=E)
    recipe_search_text.grid(row=3, column=0)

    recipe_add_remove_label.grid(row=4, column=0)
    recipe_add_entry.grid(row=5, column=0, sticky=W)
    recipe_add_button.grid(row=5, column=0, sticky=E)
    recipe_remove_entry.grid(row=6, column=0, sticky=W)
    recipe_remove_button.grid(row=6, column=0, sticky=E)
    recipe_add_remove_text.grid(row=7, column=0)

    recipe_info_label.grid(row=8, column=0)
    recipe_info_entry.grid(row=9, column=0, sticky=W)
    recipe_info_button.grid(row=9, column=0, sticky=E)

    to_main_menu_recipe_button.grid(row=7, column=1, sticky=S)

    saved_items = SQLCommands.get_chosen_recipes(currentConnection.cursor(), current_email)
    for row in saved_items:
        output = "Name: %s\nNumber: %s\n\n" % (row[0], row[1])
        recipe_add_remove_text.insert(END, output)


def search_recipe():
    global currentConnection
    global current_email

    recipe_search_text.delete("1.0", "end")
    recipe_search_input = recipe_search_entry.get()
    recipe_search_input = "%" + recipe_search_input + "%"

    if(SQLCommands.check_choseningredients(currentConnection.cursor(), current_email) > 0):
        returned_items = SQLCommands.search_recipes_with_ingredients(currentConnection.cursor(), current_email, recipe_search_input)
    else:
        print("used all")
        returned_items = SQLCommands.check_recipe(currentConnection.cursor(), recipe_search_input)

    for row in returned_items:
        output = "Name: %s\nNumber: %s\n\n" % (row[0], row[1])
        recipe_search_text.insert(END, output)

def add_recipe():
    global currentConnection
    global current_email

    recipe_add_remove_text.delete("1.0", "end")

    recipe_add_input = recipe_add_entry.get()
    print(recipe_add_input)
    if(SQLCommands.check_recipe_number(currentConnection.cursor(), recipe_add_input)):
        print("Recipe Exists")
        if(SQLCommands.check_recipenum_choseningredient(currentConnection.cursor(), recipe_add_input, current_email) == 0):
            print("It wasn't saved")
            SQLCommands.select_recipe(currentConnection.cursor(), current_email, recipe_add_input)

    saved_items = SQLCommands.get_chosen_recipes(currentConnection.cursor(), current_email)
    for row in saved_items:
        output = "Name: %s\nNumber: %s\n\n" % (row[0], row[1])
        recipe_add_remove_text.insert(END, output)


def remove_recipe():
    global currentConnection
    global current_email

    recipe_add_remove_text.delete("1.0", "end")
    recipe_remove_input = recipe_remove_entry.get()
    if(SQLCommands.check_recipenum_choseningredient(currentConnection.cursor(), recipe_remove_input, current_email)):
        SQLCommands.remove_recipe(currentConnection.cursor(), current_email, recipe_remove_input)

    saved_items = SQLCommands.get_chosen_recipes(currentConnection.cursor(), current_email)
    for row in saved_items:
        output = "Name: %s\nNumber: %s\n\n" % (row[0], row[1])
        recipe_add_remove_text.insert(END, output)


recipe_search_input = ""
recipe_add_input = ""
recipe_remove_input = ""

recipe_search_label = Label(root, text="Search for a recipe by its name")
recipe_add_remove_label = Label(root, text="Add or Remove a recipe using the barcode")

recipe_search_text = Text(root, height=10, width=35)
recipe_add_remove_text = Text(root, height=10, width=35)

recipe_search_entry = Entry(root, textvariable=recipe_search_input)
recipe_add_entry = Entry(root, textvariable=recipe_add_input)
recipe_remove_entry = Entry(root, textvariable=recipe_remove_input)

recipe_search_button = Button(root, text="Search", command=search_recipe)
recipe_add_button = Button(root, text="Add", command=add_recipe)
recipe_remove_button = Button(root, text="Remove", command=remove_recipe)

to_main_menu_recipe_button = Button(root, text="Main Menu", command=return_to_main_menu)

recipe_info_input = ""
recipe_info_label = Label(root, text="Get more info on a recipe using its number")
recipe_info_entry = Entry(root, textvariable=recipe_info_input)
recipe_info_button = Button(root, text="Get Info", command=return_to_info)


##################################################
# Recipe Info
##################################################


def go_to_info():
    global currentConnection
    global current_email

    clear_screen()

    instruction_label.configure(text="Recipe Information")
    instruction_label.grid(row=0, column=0)
    info_text.grid(row=1, column=0)
    info_return_button.grid(row=2, column=0)

    recipe_info_input = recipe_info_entry.get()
    if(len(recipe_info_input) == 0):
        return_to_recipe()
    if(SQLCommands.check_recipe_number(currentConnection.cursor(), recipe_info_input) == 0):
        print("I Left")
        return_to_recipe()
    saved_items = SQLCommands.get_recipe_info(currentConnection.cursor(), recipe_info_input)
    print(saved_items)
    print(len(saved_items))

    if(len(saved_items) != 0):
        output = "Recipe: %s\nNumber: %s\n\nDescription:\n%s\n\n" % (saved_items[0][0], saved_items[0][1], saved_items[0][2])
        info_text.insert(END, output)

        saved_items = SQLCommands.get_recipe_amounts(currentConnection.cursor(), recipe_info_input)
        for rows in saved_items:
            output = "%s %s %s\n" %(rows[1], rows[2], rows[0])
            info_text.insert(END, output)

info_text = Text(root, height = 30, width = 50)
info_return_button = Button(root, text="Recipe Selection", command=return_to_recipe)


##################################################
# Ingredient Stock Info
##################################################


def go_to_stock():
    global currentConnection
    global current_email

    clear_screen()
    instruction_label.configure(text="The Current Stock of Ingredients for Selected Recipes")
    instruction_label.grid(row=0, column=0)
    stock_text.grid(row=1, column=0)
    stock_return_button.grid(row=2, column=0)
    stock_text.delete("1.0", "end")

    saved_items = SQLCommands.get_recipe_stock_info(currentConnection.cursor(), current_email)
    for rows in saved_items:
        print(rows)
        output = "Ingredient: %s\nBarcode: %s\nPrice: $%s\n" % (rows[1], rows[0], rows[2])
        stock_text.insert(END, output)
        if(rows[3] == True):
            stock_text.insert(END, "In stock\n")
        else:
            stock_text.insert(END, "Out of stock\n")
        output = "Aisle: %s\n\n" % (rows[4])
        stock_text.insert(END, output)



stock_text = Text(root, height=30, width=50)
stock_return_button = Button(root, text="Main Menu", command=return_to_main_menu)


##################################################
# Login
##################################################


def go_to_login():
    clear_screen()
    email_entry.delete(0, "end")
    password_entry.delete(0, "end")
    instruction_label.configure(text="Please log in or create an account")
    instruction_label.grid(row=0, column=0)
    email_label.grid(row=1, column=0)
    email_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    login_button.grid(row=3, column=1)
    create_login_button.grid(row=3, column=0)
    exit_button.grid(row=4, column=0)


def try_login():
    global currentConnection
    global current_email
    email_input = email_entry.get()
    password_input = password_entry.get()
    check = SQLCommands.check_account(currentConnection.cursor(), email_input, password_input)
    if (check == 1):
        current_email = email_input
        check = SQLCommands.check_selected_store(currentConnection.cursor(), current_email)
        if(check == 1):
            return_to_main_menu()
        else:
            return_to_store()

    else:
        email_entry.delete(0, "end")
        password_entry.delete(0, "end")
        instruction_label.configure(text="Email or password is incorrect, please try again")


email_input = ""
password_input = ""
email_label = Label(root, text="Email:")
password_label = Label(root, text="Password:")
email_entry = Entry(root, textvariable=email_input)
password_entry = Entry(root, textvariable=password_input, show="*")
login_button = Button(root, text="Login", command=try_login)
create_login_button = Button(root, text="Create Login", command=go_to_create_account)
exit_button = Button(root, text="Exit", command=exit_application)

##################################################
# Start Program
##################################################


if __name__ == "__main__":
    go_to_login()
    root.mainloop()
