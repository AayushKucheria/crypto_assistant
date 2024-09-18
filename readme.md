# AI-Powered Crypto Assistant

## Overview

This project implements an AI-powered assistant that processes natural language commands related to cryptocurrency operations, specifically token swaps and cross-chain bridging. It uses OpenAI's GPT-4o model to interpret user inputs and convert them into structured outputs representing blockchain actions.

## Features

- Natural Language Understanding (NLU) for crypto operations
- Supports two main actions: swap and bridge
- Integrates with Uniswap (for swapping) and Across (for bridging)
- Supports operations on Ethereum and Arbitrum chains
- Extensible architecture for adding new actions and protocols
- Error handling and user feedback
- Input validation for token amounts and supported operations

## Requirements

- Python 3.7+
- OpenAI Python library
- An OpenAI API key

## Installation

1. Clone this repository: git clone [https://github.com/yourusername/crypto-assistant.git](https://github.com/yourusername/crypto-assistant.git)
   cd crypto-assistant
2. Install the required dependencies: pip install openai
3. Set up your OpenAI API key as an environment variable: export OPENAI_API_KEY='your-api-key-here'

## Usage

Run the main script: python crypto_assistant.py

The assistant will prompt you for input. You can enter natural language commands like:

- "Swap 100 USDT for ETH on Uniswap"
- "Bridge 50 ETH from Ethereum to Arbitrum using Across"

Type 'help' or '?' for more information about supported operations.

## Supported Operations

1. Swap tokens

   - Protocol: Uniswap
   - Chain: Ethereum
   - Parameters: tokenIn, tokenOut, amountIn
2. Bridge tokens

   - Protocol: Across
   - Chains: Ethereum, Arbitrum
   - Parameters: fromChain, toChain, token, amount

## Extension

To add new actions or protocols:

1. Update the `SUPPORTED_ACTIONS`, `SUPPORTED_PROTOCOLS`, and `SUPPORTED_CHAINS` constants.
2. Add new validation functions in the `validate_command` function.
3. Create new processing functions (e.g., `process_new_action`) for the new actions.
4. Update the `tools` list with new function definitions for the AI model.
5. Modify the `process_ai_response` function to handle the new actions.

## Error Handling

The assistant provides informative error messages for:

- Unsupported actions, protocols, or chains
- Invalid token amounts
- General processing errors

## Future Enhancements

- Implement a recommendation system based on user portfolio
- Add support for more DeFi protocols and chains
- Integrate with real-time price feeds for token conversions
- Implement multi-step operations (e.g., swap then bridge)


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a prototype and should not be used for actual financial transactions without proper security audits and real-world testing.
