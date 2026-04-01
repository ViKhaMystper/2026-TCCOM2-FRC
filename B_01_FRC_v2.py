import pandas
from tabulate import tabulate
from datetime import date
import math

# Function go here
def make_statement(statement, decoration):
    """Emphasizes headings by adding decoration at the start and end"""
    return f"{decoration * 3} {statement} {decoration * 3}"

def yes_no_check(question):
    """Check user enter yes / y or no / n"""
    while True:
        response = input(question).lower()
        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes (y) or no (n). \n")

def instruction():
    print(make_statement("Instruction", "ℹ️"))

    print('''This program will ask you for... 
    - The name of your product 
    - How many items you use that expenses 
    - The costs for each component of the product 
    - Do you have fixed expenses (if you have 
      fixed expenses, it will ask you what they are).
    - How much money of your profit you want to make (profit goal)

It will also ask you how much the recommended sales price should 
be rounded to.

The program outputs an itemised list of the variable and fixed 
expenses (which includes the subtotals for these expenses). 

Finally it will tell you how much you should sell each item for 
to reach your profit goal. 

The data will also be written to a text file which has the 
same name as your product and today's date.
''')

def not_blank(question):
    """Check that a user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("This cannot be blank. Please try again.")

def num_check(question, num_type="float", exit_code = None):
    """Check users enter an integer / float that is more than zero
    (or the optional exit code)"""

    if num_type == "float":
        error = "Please enter an number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:

        response = input(question)

        # check for the exit code and return it if entered
        if response == exit_code:
            return response


        # Check datatype is correct and that number is more than 0
        try:
            if num_type == "float":
                response = float(response)
            else:
                response = int(response)


            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

def get_expenses(exp_type, how_many=1):
    """Gets a variable / fix expenses and outputs pandas (as a string) and a
    subtotal of the expenses."""

    # List for panda
    all_item = []
    all_amount = []
    all_dollar_per_item = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_item,
        "Amount": all_amount,
        "$ / Item": all_dollar_per_item
    }

    # Defaults for fixed expenses
    amount = how_many # how many defaults to 1
    how_much_question = "How much? $"

    # loop to get expenses
    while True:
        # Get item name and check it's not blank
        item_name = not_blank("Item name: ")

        # Checks users enter at least one variable expenses
        if exp_type == "variable" and item_name == "xxx" and len(all_item) == 0:
            print("Oops - You have not entered anything. "
                  "You need at least one item.")
            continue

        # End loop when users enter exit code
        elif item_name == "xxx":
            break

        # Get variable expenses item amount <enter> default to number of products being made
        if exp_type == "variable":

            amount = num_check(f"How many items use this expenses: ",
                               "integer","")

            # Allow users to push <enter> to default to number of items being made
            if amount == "":
                amount = how_many

            how_much_question = "Price for one? $"


        # Get price for item (question customized depending on expense type)
        price_for_one = num_check(how_much_question, "float")

        all_item.append(item_name)
        all_amount.append(amount)
        all_dollar_per_item.append(price_for_one)

    # Make panda
    expense_frame = pandas.DataFrame(expenses_dict)

    # Calculate Row Cost
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    # Calculate subtotal
    subtotal = expense_frame['Cost'].sum()

    # Apply currency formatting to currency columns
    add_dollars = ['$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # Make expense frame into a string with the desired columns
    if exp_type.lower() == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)

    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']],
                                  headers='keys', tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal

def currency(x):
    """Formats numbers as currency ($#,##)"""
    return "${:.2f}".format(x)

def profit_goal(total_cost):
    """Calculate profit goal work out profit goal and total sales required"""
    # Initialize variables and error message
    error = "Please enter a valid profit goal \n"

    valid = False
    while not valid:

        # Ask for profit goal...
        response = not_blank("What is your profit goal (e.g. $500 or 50%): ")

        # Check if first character $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything after the %)
            amount = response[:-1]

        else:
            # Set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no_check(f"Do you mean ${amount:.2f}. ie {amount:.2f} dollars? , y / n:")

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no_check(f"Do you mean {amount}%? , y / n:")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # Return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_cost
            return goal

def round_up(amount, round_val):
    """Rounds amount to desired whole number"""
    return float(math.ceil(amount / round_val)) * round_val


# Main routine goes here

# Initialise variables...

# Assume we have no fixed expenses for now
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement("Fund Raising Calculator", "💰"))

print()
want_instruction = yes_no_check("Do you want to see the instruction? ")
print()

if want_instruction == "yes":
    instruction()

print()

# Get products details...
product_name = not_blank("Product name: ")
quantity_made = num_check("Quantity being made: ", "integer")

# Get variables expenses...
print("Let's get the variable expenses...")
variable_expenses = get_expenses("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

# Ask users if they have fixed expenses and retrieve them
print()
has_fixed = yes_no_check("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    # If the user has not entered any fixed expenses, set empty panda to "" so
    # that it does not display!

    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""


total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"


# Get profit Goal here
target = profit_goal(total_expenses)
sale_target = total_expenses + target


# Calculate minimum selling price and round it to nearest desired dollar amount
selling_price = (total_expenses + target) / quantity_made
round_to = num_check("Round to: ", "integer")
suggested_price = round_up(selling_price, round_to)

# String output here

# Get current date for heading and file name
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Headings / strings...
main_heading_string = make_statement(f"Fund Raising Calculator "
                                     f"({product_name}, {day}/ {month}/ {year})", "=")

quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expenses ", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"


# set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement(f"Fixed Expenses ", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: ${fixed_subtotal:.2f}"

# Set fixed cost strings to blank if we don't have fixed costs
else:
    fixed_heading_string = make_statement("You have no Fixed Expenses ", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

selling_price_heading = make_statement("Selling Prices Calculation", "-")
profit_goal_string = f"Profit Goal: ${target:.2f}"
sale_target_string = f"\nTotal Sales Needed: ${sale_target:.2f}"

minimum_price_string = f"Minimum Selling Price: ${selling_price:.2f}"
suggested_price_string = make_statement(f"Suggested Selling Price: "
                                        f"${suggested_price:.2f}","*")

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string,
            profit_goal_string, sale_target_string,
            minimum_price_string, "\n", suggested_price_string]

# Print area
print()
for item in to_write:
    print(item)

# Create file to hold data (add .txt extension)
file_name = f"{product_name}_{day}_{month}_{year}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w")

# Write the item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")