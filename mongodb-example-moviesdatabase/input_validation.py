def input_int(prompt="Please enter a whole number: ",
              error="That's not a valid number. Try again.", **kwargs):
    # Get an integer input from the user with optional range validation.
    while True:
        try:
            value = int(input(prompt))
            if _validate_range(value, **kwargs):
                return value
        except ValueError:
            pass
        print(error)


def input_float(prompt="Please enter a decimal number: ",
                error="That's not a valid decimal. Try again.", **kwargs):
    # Get a float input from the user with optional range validation.
    while True:
        try:
            value = float(input(prompt))
            if _validate_range(value, **kwargs):
                return value
        except ValueError:
            pass
        print(error)


def input_string(prompt="Please enter some text: ",
                 error="Input cannot be empty. Try again.",
                 valid=lambda x: bool(x.strip())):
    # Get a string input from the user, with optional validation.
    while True:
        user_input = input(prompt).strip()
        if valid(user_input):
            return user_input
        print(error)


def y_or_n(prompt="Please answer yes or no: ",
           error="Invalid input. Please type 'yes' or 'no'."):
    # Ask the user a yes/no question and return True/False based on the answer.
    valid_yes = {"yes", "y"}
    valid_no = {"no", "n"}
    while True:
        answer = input(prompt).strip().lower()
        if answer in valid_yes:
            return True
        if answer in valid_no:
            return False
        print(error)


def select_item(choices, prompt="Please select an item: ",
                error="Invalid choice. Try again.", mapping=None):
    # Allow the user to select an item from a list of choices.
    if mapping:
        choices = {k.lower(): v for k, v in mapping.items()}
    else:
        choices = {item.lower(): item for item in choices}

    while True:
        selection = input(prompt).strip().lower()
        if selection in choices:
            return choices[selection]
        print(error)


def input_value(type="string", **kwargs):
    # A single interface to call any of the input functions.
    functions = {
        "int": input_int,
        "float": input_float,
        "string": input_string,
        "y_or_n": y_or_n,
        "select": select_item,
    }
    if type not in functions:
        raise ValueError(f"Invalid input type: {type}")
    return functions[type](**kwargs)


# Helper function for range validation
def _validate_range(value, ge=None, gt=None, le=None, lt=None):
    # Check if a number satisfies optional range constraints.
    if ge is not None and value < ge:
        print(f"Value must be >= {ge}.")
        return False
    if gt is not None and value <= gt:
        print(f"Value must be > {gt}.")
        return False
    if le is not None and value > le:
        print(f"Value must be <= {le}.")
        return False
    if lt is not None and value >= lt:
        print(f"Value must be < {lt}.")
        return False
    return True
