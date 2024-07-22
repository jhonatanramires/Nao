import os
from dotenv import load_dotenv, set_key # type: ignore

def save_args_to_env(args):
    """
    Save all arguments from an argparse.Namespace object to a .env file.

    :param args: argparse.Namespace object containing the arguments
    """
    # Define the path for the .env file (in the current directory)
    dotenv_path = os.path.join(os.getcwd(), '.env')

    # Load existing .env file or create it if it doesn't exist
    load_dotenv(dotenv_path)

    # Iterate through all attributes in the args object
    for arg_name, arg_value in vars(args).items():
        # Convert the argument name to uppercase for .env convention
        env_var_name = arg_name.upper()
        
        # Convert the value to string, as .env files store everything as strings
        env_var_value = str(arg_value)
        
        # Set the key-value pair in the .env file
        set_key(dotenv_path, env_var_name, env_var_value)

    print(f"All arguments have been saved to {dotenv_path}")