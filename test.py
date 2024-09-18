import unittest
from crypto_assistant import process_nl_input

class TestCryptoAssistant(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning: {self._testMethodName}")

    def test_basic_swap(self):
        result, _ = process_nl_input("Swap 100 ETH for USDT on Uniswap")
        self.assertIsNotNone(result)
        self.assertEqual(result["action"].lower(), "swap")
        self.assertEqual(result["params"]["token_in"].lower(), "eth")
        self.assertEqual(result["params"]["token_out"].lower(), "usdt")
        self.assertEqual(result["params"]["amount_in"], "100")
        self.assertEqual(result["params"]["protocol"].lower(), "uniswap")

    def test_swap_with_misspelling(self):
        result, _ = process_nl_input("Swop 100 ETH for USDT on Uniswap")
        self.assertIsNotNone(result)
        self.assertEqual(result["action"].lower(), "swap")
        self.assertEqual(result["params"]["token_in"].lower(), "eth")
        self.assertEqual(result["params"]["token_out"].lower(), "usdt")

    def test_swap_with_wrong_amount(self):
        result, message = process_nl_input("Swap -100 ETH for USDT on Uniswap")
        self.assertIsNone(result)
        self.assertIsNotNone(message)

    def test_swap_same_currency(self):
        result, message = process_nl_input("Swap 100 ETH for ETH on Uniswap")
        self.assertIsNone(result)
        self.assertIsNotNone(message)

    def test_basic_bridge(self):
        result, _ = process_nl_input("Bridge 50 ETH from Ethereum to Arbitrum")
        self.assertIsNotNone(result)
        self.assertEqual(result["action"].lower(), "bridge")
        self.assertEqual(result["params"]["from_chain"].lower(), "ethereum")
        self.assertEqual(result["params"]["to_chain"].lower(), "arbitrum")
        self.assertEqual(result["params"]["token"].lower(), "eth")
        self.assertEqual(result["params"]["amount"], "50")

    def test_bridge_same_protocols(self):
        result, message = process_nl_input("Bridge 50 ETH from Ethereum to Ethereum")
        self.assertIsNone(result)
        self.assertIsNotNone(message)

    def test_bridge_incorrect_protocol(self):
        result, message = process_nl_input("Bridge 50 ETH from Ethereum to Solana")
        self.assertIsNone(result)
        self.assertIsNotNone(message)

    # An example test where the LLM notes success which our backend should catch failure
    def test_bridge_incorrect_currency(self):
        result, message = process_nl_input("Bridge 50 EUR from Ethereum to Arbitrum")
        self.assertIsNone(result)
        self.assertIsNotNone(message)

if __name__ == '__main__':
    unittest.main(verbosity=1)