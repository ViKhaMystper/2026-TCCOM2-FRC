def not_blank(question):
    """Check that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again. \n")

def num_check(question, num_type="float", exit_code = None):
    """Check users enter an integer / float that is more than zero
    (or the optional exit code)"""

    if num_type == "float":
        error = "Oops - Please enter an number more than 0."
    else:
        error = "Oops - Please enter an integer more than 0."

    while True:
        try:

            if num_type == "float":
                response = float(input(question))
            else:
                response = int(input(question))

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

def get_expenses(exp_type):
    """Gets a variable / fix expenses and outputs pandas (as a string) and a
    subtotal of the expenses."""

    # List for panda
    all_item = []

    # Expenses dictionary
    while True:
        item_name = not_blank("Item name: ")

        # Checks users enter at least one variable expenses
        if ((exp_type == "variable" and item_name == "xxx")
                and len(all_item) == 0):
            print("Oops - You have not entered anything. "
                  "You need at least one item.")
            continue

        elif item_name == "xxx":
            break

        all_item.append(item_name)

    # return all items for now so we can check loop
    return all_item


# Main routine start here
print("Getting variable costs...")
variable_expenses = get_expenses("variable")
num_variable = len(variable_expenses)
print(f"You entered {num_variable} items.")
print()

print("Getting Fixed Costs...")
fixed_expenses = get_expenses("fixed")
num_fixed = len(fixed_expenses)
print(f"You entered {num_fixed} items.")