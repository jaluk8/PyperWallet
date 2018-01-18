from pyperlib import cliwallet, helper


class BaseCliTest(helper.CliTestCase):
    """Provide an interface for cli tests."""

    def make_wallet(self, args):
        """Create a wallet from args."""
        return cliwallet.CliWallet(("pyperwallet",) + args)


class TestErrors(BaseCliTest):
    """Test that cliwallet returns certain errors."""

    def run_wallet(self, w, stdin):
        """Run the wallet with some stdin."""
        self.cli_test(w.run, stdin=stdin)

    def do_test(self, stdin, *args):
        """Create a wallet  and assert that it errors."""
        w = self.make_wallet(args)
        self.assertRaises(SystemExit, self.run_wallet, w, stdin)

    def test_all(self):
        """Check various args that should error."""
        self.do_test(["hi"], "-i", "prompt")
        self.do_test(["17nArmyTmUGw9uPk3HsCabRj5wN7LfWSmr"],
                     "-i", "prompt")
        self.do_test(["17nArmyTmUGw9uPk3HsCabRj5wN7LfWSm0"],
                     "-i", "prompt")


class TestOutputs(BaseCliTest):
    """Test that cliwallet returns the expected output format."""

    in1 = ["17nArmyTmUGw9uPk3HsCabRj5wN7LfWSmR"]
    out1 = """Coin name: Bitcoin
Compressed: True

Public address: 17nArmyTmUGw9uPk3HsCabRj5wN7LfWSmR
"""

    in2 = ["testwalletpleasedontuse",
           "testwalletpleasedontuse"]
    out2 = """Coin name: Bitcoin
Compressed: False

Private WIF key: 5HyK3DyhYiuwy1tgJXTGyrVyNJqs1pPiXGe3YpMC6uyKiutuCRV
Private hex key: 147E1F5B49A4810A33E6525DA2E0E35BA220F9A5FE46585693EFCE48FA5CF\
305

Public address: 1LX8yo6YCQCFpAGAc797kwVqya4ryjDB81
Public hex key: 04FE22B51BA42A72C90C85F74CF9D4088496620991535D92CF6768DEC8BBD1\
4A4AB01675E556AEBD6AD47A4035C71EA22DFFF1D2DABD1F1396F40D16571FD9D5B0
"""

    in3 = ["147E1F5B49A4810A33E6525DA2E0E35BA220F9A5FE46585693EFCE48FA5CF305"]
    out3 = """Coin name: Ethereum
Compressed: True

Private WIF key: 147E1F5B49A4810A33E6525DA2E0E35BA220F9A5FE46585693EFCE48FA5CF\
305
Private hex key: 147E1F5B49A4810A33E6525DA2E0E35BA220F9A5FE46585693EFCE48FA5CF\
305

Public address: 0x9ab50410588eEa933ab5b14f85f2791FD7c0bc9d
Public hex key: 02FE22B51BA42A72C90C85F74CF9D4088496620991535D92CF6768DEC8BBD1\
4A4A
"""

    def do_test(self, stdin, stdout, *args):
        """Create a wallet and check its output."""
        w = self.make_wallet(args)
        self.cli_test(w.run, stdout=stdout, stdin=stdin)

    def test_all(self):
        """Check various args and their output."""
        self.do_test(self.in1, self.out1, "-i", "prompt")
        self.do_test(self.in2, self.out2, "--debug", "-i", "brain",
                     "--compression", "no")
        self.do_test(self.in3, self.out3, "-i", "prompt", "-c", "ethereum")
