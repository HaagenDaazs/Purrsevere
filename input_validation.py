def validate_input(input_type, data_type=str, allowed_values=None):
    """ generic input validation for all types of user input 
    
    Primary Author: Jadon Tallapally
    
    techniques: conditional expressions
    
    Args:
        input_type(str or int): Any type of input that the game requests from 
                the user
        data_type(str or int): The data type to convert the input into
                (default = str)
        allowed_values(list or set): A collection of valid values that the given 
            input have to match (default = None)
       
    Returns:
        converted_value(str or int): The validated and converted input value 
        that matches the specified data_type
        
    Side Effects:
        prints to the console error messages if input is invalid:
        if the data type is invalid (if valueError is caught), it prints 
            "Please enter a valid (data type)"
        if the data type is not in the collection, it prints "Input Invalid! 
            Try again!"
        
    """
    while True:
        response = input(input_type)
        try:
            input_value = response.lower() if data_type is str else response
            converted_value = input_value if data_type is str else \
                data_type(input_value)
        
        except ValueError:
            print(f"Please enter a valid {data_type.__name__}")
            continue
        
        if allowed_values is not None and converted_value not in allowed_values:
            print(f"Input Invalid! Try again!")
            continue
        return converted_value         
