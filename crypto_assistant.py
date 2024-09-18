import openai
from openai import OpenAI
import json
from decimal import Decimal, InvalidOperation
import os

# Constants
API_KEY = os.environ.get("OPENAI_API_KEY")
SUPPORTED_ACTIONS = ['swap', 'bridge']
SUPPORTED_PROTOCOLS = ['uniswap', 'across']
SUPPORTED_CHAINS = ['ethereum', 'arbitrum']
MAX_TOKEN_AMOUNT = Decimal('1000000')  # 1 million tokens
MIN_TOKEN_AMOUNT = Decimal('0.000001')  # 1 millionth of a token

# OpenAI client initialization
client = OpenAI(api_key=API_KEY)

HELP_TEXT = """
    Supported Actions:
    1. Swap tokens
    2. Bridge tokens
    
    Supported Protocols:
    - Uniswap (for swapping)
    - Across (for bridging)
    
    Supported Chains:
    - Ethereum
    - Arbitrum
    
    Example Commands:
    1. Swap 100 USDT for ETH on Uniswap
    2. Bridge 50 ETH from Ethereum to Arbitrum using Across"""

# System message for the AI
SYSTEM_MESSAGE = """
You are a helpful assistant for crypto operations. 

{HELP_TEXT}

If the user asks for unsupported actions or provides unclear inputs, guide them towards these supported operations.
"""

# Define the tools for swap and bridge actions
tools = [
    {
        "type": "function",
        "function": {
            "name": "swap",
            "description": "Swap tokens on Uniswap (Ethereum)",
            "parameters": {
                "type": "object",
                "properties": {
                    "token_in": {"type": "string", "description": "Token to swap from"},
                    "token_out": {"type": "string", "description": "Token to swap to"},
                    "amount_in": {"type": "string", "description": "Amount of token_in to swap"},
                    "protocol:": {"type": "string", "description": "The protocol to be used"}
                },
                "required": ["token_in", "token_out", "amount_in", "protocol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bridge",
            "description": "Bridge tokens from one chain to another using Across protocol",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_chain": {"type": "string", "description": "Source chain"},
                    "to_chain": {"type": "string", "description": "Destination chain"},
                    "token": {"type": "string", "description": "Token to bridge"},
                    "amount": {"type": "string", "description": "Amount of token to bridge"},
                },
                "required": ["from_chain", "to_chain", "token", "amount"]
            }
        }
    }
]

def validate_amount(amount_str: str) -> tuple[bool, str]:
    """Validate the token amount."""
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            return False, "The amount must be greater than zero."
        if amount < MIN_TOKEN_AMOUNT:
            return False, f"The amount is too small. Minimum amount is {MIN_TOKEN_AMOUNT}."
        if amount > MAX_TOKEN_AMOUNT:
            return False, f"The amount is too large. Maximum amount is {MAX_TOKEN_AMOUNT}."
        return True, str(amount)
    except InvalidOperation:
        return False, "Invalid amount. Please enter a valid number."

def generate_error_message(error_type: str, value: str) -> str:
    """Generate an informative error message based on the type of error."""
    if error_type == 'action':
        return f"I'm sorry, but the '{value}' action is not supported. Currently, I can help with {', '.join(SUPPORTED_ACTIONS)} operations. Would you like to try one of these?"
    elif error_type == 'protocol':
        return f"I apologize, but {value} is not a supported protocol. Currently, I can work with {', '.join(SUPPORTED_PROTOCOLS)}. Would you like to use one of these instead?"
    elif error_type == 'chain':
        return f"I'm sorry, but {value} is not a supported blockchain. Currently, I can work with {', '.join(SUPPORTED_CHAINS)}. Would you like to try with one of these chains?"
    else:
        return "I couldn't understand your request. Could you please rephrase it in terms of swapping or bridging tokens?"
    
def validate_swap(function_args: dict) -> tuple[bool, str]:
    """Validate swap operation arguments."""
    if function_args.get('protocol', '').lower() not in SUPPORTED_PROTOCOLS:
        return False, generate_error_message('protocol', function_args.get('protocol', ''))
    is_valid, amount_message = validate_amount(function_args.get('amount_in', '0'))
    if not is_valid:
        return False, f"Invalid amount for swapping: {amount_message}"
    return True, amount_message

def validate_bridge(function_args: dict) -> tuple[bool, str]:
    """Validate bridge operation arguments."""
    for chain in [function_args.get('from_chain', ''), function_args.get('to_chain', '')]:
        if chain.lower() not in SUPPORTED_CHAINS:
            return False, generate_error_message('chain', chain)
    is_valid, amount_message = validate_amount(function_args.get('amount', '0'))
    if not is_valid:
        return False, f"Invalid amount for bridging: {amount_message}"
    return True, amount_message
    
def get_ai_response(input_text: str) -> openai.types.chat.ChatCompletion:
    """Get AI response for the given input."""
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": input_text}
    ]
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

def validate_command(function_name: str, function_args: dict) -> tuple[bool, str]:
    """Validate the command based on the function name."""
    if function_name == 'swap':
        return validate_swap(function_args)
    elif function_name == 'bridge':
        return validate_bridge(function_args)
    else:
        return False, f"Unsupported action: {function_name}"
    
def process_swap(function_args: dict) -> dict:
    """Process a swap command."""
    return {
        "action": "swap",
        "protocol": "uniswap",
        "chain": "ethereum",
        "params": function_args
    }

def process_bridge(function_args: dict) -> dict:
    """Process a bridge command."""
    return {
        "action": "bridge",
        "protocol": "across",
        "chain": f"{function_args['from_chain']}->{function_args['to_chain']}",
        "params": function_args
    }

def process_ai_response(response: openai.types.chat.ChatCompletion) -> tuple[dict | None, str]:
    """Process the AI response and return structured output or guidance."""

    # print(response.choices[0].message)

    if not response.choices[0].message.tool_calls:
        # Return the AI's message content if there are no tool calls
        return None, response.choices[0].message.content

    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    
    # Manually validate the command as well
    is_valid, message = validate_command(function_name, function_args)
    if not is_valid:
        return None, message
    
    result = None
    if function_name == 'swap':
        result = process_swap(function_args)
    elif function_name == 'bridge':
        result = process_bridge(function_args)

    if result is None:
        return None, f"Unsupported action: {function_name}"

    return result, "Operation processed successfully."
        

def process_nl_input(input_text: str) -> tuple[dict | None, str | None]:
    """Process natural language input and return structured output or guidance."""

    if input_text.lower() in ['help', '?']:
        return None, HELP_TEXT
    try:
        ai_response = get_ai_response(input_text)
        return process_ai_response(ai_response)
    except Exception as e:
        return None, f"An error occurred while processing your request: {str(e)}. Could you please try again?"


def main():
    print("Welcome to the Crypto Assistant! I can help you with swapping and bridging tokens.")
    print("Type 'help' or '?' for more information, or 'exit' to end the conversation.")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == 'exit':
            print("Assistant: Thank you for using the Crypto Assistant. Goodbye!")
            break
        
        result, message = process_nl_input(user_input)
        if result:
            print(f"Assistant: Operation processed successfully.")
            print(f"Structured output: {json.dumps(result, indent=2)}")
        elif message:
            print(f"Assistant: {message}")
        else:
            print("Assistant: I'm sorry, I couldn't process that request. Could you try again?")

if __name__ == "__main__":
    main()