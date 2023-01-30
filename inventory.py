from tabulate import tabulate
import tkinter as tk
import os

#========The beginning of the class==========

class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)

    def get_cost(self):

        return self.cost

    def get_quantity(self):
        
        return self.quantity

    def __str__(self):
        
        return f'''
Country:                        {self.country}
Code:                           {self.code}
Product:                        {self.product}
Cost:                           {self.cost}
Quantity:                       {self.quantity}
        '''


#=============Shoe list===========

shoe_list = []

#==========Functions outside the class==============

def read_shoes_data():

    try:

        f = open("inventory.txt", "r")

        f.readline()    # to skip the first line of the file

        for line in f:

            shoe = line.split(",")

            shoe_list.append(Shoe(shoe[0], shoe[1], shoe[2], shoe[3], shoe[4]))
        
        f.close()

    except IOError:

        print("An error occurred when reading the file.")
    
    except ValueError:

        print("An error occurred when parsing the file.")


def capture_shoes():

    window.destroy()    # removes the window
    
    print("Enter the information for the new shoes \n")

    country = input("Country: ")

    while True: # ensures code is not already in use

        code = input("Code: ")
        result = filter(lambda shoe: shoe.code == code, shoe_list)

        shoe = next(result, None)
        if shoe is None:
            break
        else:
            print("Code already in use.")

    product = input("Product: ")
    
    cost = ""
    while cost == "":   # ensures cost is given in correct format
        try:
            cost = int(input("Cost (ZAR): "))
        except ValueError:
            print("Please give cost in Rand as an integer")
    
    quantity = ""
    while quantity == "":   # ensures quantity is given is given in correct format
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Please give quantity as an integer")
    
    shoe_list.append(Shoe(country, code, product, cost, quantity))


def view_all(): # displays the information in a table

    window.destroy()
    
    data = [[p.country, p.code, p.product, p.cost, p.quantity] for p in shoe_list]
    print(tabulate(data, headers=['Country', 'Code', 'Product', 'Cost', 'Quantity']))
    print()


def re_stock(): # finds the shoe with the lowest stock count and allows the user increase quantity

    window.destroy()
    
    min_quantity = min(shoe_list, key=lambda shoe: int(shoe.quantity))

    print("The shoe with the lowest current stock:")
    print(min_quantity)

    increase = -1
    while increase < 0:
        try:
            increase = int(input("How many pairs should be added to stock: "))
        except:
            print("Quantity entered should be a positive integer.")
    
    min(shoe_list, key=lambda shoe: int(shoe.quantity)).quantity += increase


def search_shoe():  # if the code entered by the user matches one of the objects, this object is displayed

    window.destroy()
    
    code_search = input("Enter the code of the shoe for which you want to display information: ")
    
    result = filter(lambda shoe: shoe.code == code_search, shoe_list)

    shoe = next(result, None)
    if shoe is not None:
        print(shoe)
    else:
        print("Shoe not found.")


def value_per_item():

    window.destroy()
    
    data = []
    total_value = 0
    for shoe in shoe_list:

        value =  shoe.get_cost() * shoe.get_quantity()  # formula for stock value

        total_value += value

        data.append([shoe.country, shoe.code, shoe.product, value])

    print(tabulate(data, headers=['Country', 'Code', 'Product', 'Total Value of remaining stock']))
    print()
    print(f"Total value of all stock is R{total_value}")
    print()



def highest_qty():

    window.destroy()
    
    max_quantity = max(shoe_list, key=lambda shoe: int(shoe.quantity))

    print("The shoe with the greatest current stock is:")
    print(max_quantity)


#==========Main Menu=============

read_shoes_data()

# I wanted for the user choice to be selected from a menu rather than typed in.
# I was having problems doing this, as the destroy() method prevented further use of the mainloop() method;
# also, using the withdraw() method prevented the functions from returning. The solution was to create a class,
# and then call instances of the class; this allows mainloop() and destroy() to be used multiple times:

class MenuWindow(tk.Tk):  # each instance of class has six buttons, each of which calls one of the functions
    def __init__(self):
        super().__init__()
        
        self.button1 = tk.Button(self, text="View all", command=view_all)
        self.button2 = tk.Button(self, text="Add shoe", command=capture_shoes)
        self.button3 = tk.Button(self, text="Use shoe code to search for shoe", command=search_shoe)
        self.button4 = tk.Button(self, text="Stock values", command=value_per_item)
        self.button5 = tk.Button(self, text="Restock item", command=re_stock)
        self.button6 = tk.Button(self, text="Highest quantity", command=highest_qty)

        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()
        self.button5.pack()
        self.button6.pack()


# start the event loop
while True:

    window = MenuWindow() # creates instance of menu window
    window.title("Select an option:")
    window.mainloop()   # opens menu window

    enter_continue = input("Press enter to continue")
    os.system('cls')    # clears screen so that information is always displayed at the top

