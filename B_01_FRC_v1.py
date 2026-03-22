import pandas
from tabulate import tabulate
from datetime import date


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

    print('''
For each ticket holder enter...
- Their name
- Their age
- The payment method (cash / credit)

The programme will record the ticket sale and calculate 
the ticket cost (and the profit).

Once you have either sold all of the tickets or enter the exit code ('xxx'), the
programme will display the ticket sales information and write the data 
to a text file.

It will also choose one lucky ticket holder who wins the 
draw (their ticket is free)
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

            while True:
                amount = num_check(f"How many items use this expenses: ",
                               "integer","")

                # Allow users to push <enter> to default to number of items being made
                if amount == "":
                    amount = how_many

                # Check they didn’t enter more than quantity made
                elif amount > how_many:
                    print(f"Sorry, you can't enter more than the quantity of the product ({how_many}). Please try again.")
                    continue
                break
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
    add_dollars = ['Amount', '$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # Make expense frame into a string with the desired columns
    if exp_type == "Variable":
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

quantity_sting = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expenses ", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"


# Get up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement(f"Fixed Expenses ", "-")
    fixed_subtotal_string = f"Variable Expenses Subtotal: ${fixed_subtotal:.2f}"

# Set fixed cost strings to blank if we don't have fixed costs
else:
    fixed_heading_string = make_statement("You have no Fixed Expenses ", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_sting,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string]

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