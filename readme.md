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

1. Clone this repository: `git clone https://github.com/yourusername/crypto-assistant.git`
   `cd crypto-assistant`
2. Install the required dependencies: `pip install openai`
3. Set up your OpenAI API key as an environment variable: `export OPENAI_API_KEY='your-api-key-here'`

## Usage

Run the main script: `python crypto_assistant.py`

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
2. If action, add new validation and processing functions.
3. Update the `tools` list with new function definitions for the AI model.
4. Update the `help` and `system message` with the new additions.

## Error Handling and Security

- The assistant uses AI-generated responses for user-friendly error messages and guidance.
- Backend functions implement strict validation to prevent unauthorized or invalid operations, overriding AI decisions if necessary.
- This dual approach allows for a flexible user experience while maintaining robust security measures.

## Future Enhancements

- Add support for multi-step conversations and operations (e.g., swap then bridge)
- Expand supported protocols and chains
- Implement more sophisticated portfolio analysis and action suggestion.
  - A basic system would include a set of heuristics that would periodically be measured against user data and suggest actions based on that information.
  - A fancier version would:
    - conduct portfolio analysis to measure asset distribution, diversification, historical performance
    - include more comprehensive "opportunity detectors" such as idle balance, gas optimization, etc
    - learn user preferences over time (tokens, risk tolerance, period, etc)
    - have a feedback loop to track which recommendations are acted upon

## License

This project is licensed under the MIT License.

## Disclaimer

This is a prototype and should not be used for actual financial transactions without proper security audits and real-world testing.
