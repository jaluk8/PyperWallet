from pyperlib import coins, coinutil, data
from pyperlib.coins.basecoin import Coin as BaseCoin
from unittest import TestCase


class TestBaseCoin(TestCase):
    """A TestCase for the BaseCoin class."""

    def do_constructor(self, *args, **kwargs):
        """Check that the constructor throws the correct error."""
        self.assertRaises(NotImplementedError, BaseCoin, *args, **kwargs)

    def test_set(self):
        """Check all possible versions of the constructor."""
        self.do_constructor()


class TestAllCoins(TestCase):
    """A TestCase for every Coin module."""

    example_keys = None

    def check_gen(self, Coin):
        """Generate Coin and check that it loads correctly."""
        for _ in range(5):
            c = Coin()

            self.assertIsInstance(c.wif_string(), str)
            self.assertIsInstance(c.addr_string(), str)

            if Coin.has_privacy:
                view = c.view
                self.assertIsInstance(c.view_string(), str)
            else:
                view = None

            self.check_load(Coin, None, None, None, c.wif, view, c.addr)

    def check_load(self, Coin, wif_str, view_str, addr_str, wif, view, addr):
        """Load Coin from various keys and check correctness."""
        c1 = Coin(key=wif)
        self.assertEqual(c1.wif, wif)
        self.assertEqual(c1.addr, addr)
        if Coin.has_privacy:
            self.assertEqual(c1.view, view)

        c2 = Coin(key=addr)
        self.assertEqual(c2.wif, None)
        self.assertEqual(c2.addr, addr)
        if Coin.has_privacy:
            self.assertEqual(c2.view, None)

        if Coin.has_privacy:
            c3 = Coin(key=view)
            self.assertEqual(c3.wif, None)
            self.assertEqual(c3.addr, None)
            self.assertEqual(c3.view, view)

        if wif_str is not None:
            c4 = Coin(key=wif_str)
            self.assertEqual(c4.wif, wif)

        if addr_str is not None:
            c5 = Coin(key=addr_str)
            self.assertEqual(c5.addr, addr)

        if view_str is not None and Coin.has_privacy:
            c6 = Coin(key=view_str)
            self.assertEqual(c6.view, view)

    def get_key(self, name, Coin):
        """Retrieves the example values for name."""
        key = self.example_keys[name]

        wif = Coin.str2wif(key[0])
        addr = Coin.str2addr(key[2])
        if Coin.has_privacy:
            view = Coin.str2view(key[1])
        else:
            view = None

        return key[0], key[1], key[2], wif, view, addr

    def test_all(self):
        """Gets a list of all implemented coins and runs check_coin."""
        if self.example_keys is None:
            self.example_keys = example_keys

        cf = coinutil.CoinFactory
        for name in cf.list():
            Coin = cf.get(name)
            self.check_gen(Coin)

            if name in self.example_keys:
                key = self.get_key(name, Coin)
                self.check_load(Coin, *key)


class TestValidation(TestAllCoins):
    """A TestCase for checking that checksum validation works."""

    example_keys = {  # These all have minor errors included
        "bitcoin": ("KyF4khaPVK9YeMBUukYKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU",
                    None, "1PYqAUK4q8Lbq32o32ouyQMUFkzszw6ywx"),
        "litecoin": ("T3hvqLBBEtBui8Leo9bhezChRggpPuqVxBP2A9svN8gYrig13GDZ",
                     None, "LWUhrUrbUMZTsNqQkCtuMwsr9pTskCLrVt"),
        "bitcoincash": ("5JNrhoR2HJ1fH5ts1n2D77o35MrVCEj3gQvBWTc3oZi55uuMu34",
                        None, "13gU9r4cKRvLMKgFtt5nuMYJ6SEyPBjwiD"),
        "dash": ("XCZtcGqHxmFAmfxQhKmra9AwkESEHknu5jTAKEgSTAFypc93jovp",
                 None, "XwEMaB6n2CPxKS9poY1DZCZEv7v8woJmWu"),
        "dogecoin": ("6JDNEPxEquFzs5qEMjHkGAjkGU3VbSiQkGaz7FfDhTwxwd88tL5",
                     None, "DL95V4VvxbvhVdeih8ovaXMHijh2rphiXb"),
        "feathercoin": ("N9mVytYSM1cDEecUKv68mis5WF8cC9Xzi6nwMm9GAExJ4wmNDU6d",
                        None, "6fQZRM4i5NWs5YXEdQgAKpjrGfwjZQnbje"),
        "vertcoin": ("L5f9KLMVxanA6aVANckLmCcCb5T93uBGkiQauDBCVBXfD3JQnH9e",
                     None, "Vy47znT6TubeunhMau9v4ZuKrDdbfAJHKG"),
        "zcash": ("Kx62UU7eJP4rCtaU1N8zy34cWnkj2CoFfpbetMbSD9hoY1gDLvdL",
                  None, "t1WCf2xoYaeUzHKjdLCxjHL2C4W2S6jZMSQ"),
        "ethereum": ("ab2aeb09578892b1658ee924ae166772c57ce4b77685eca3ea6647da"
                     "84b96287", None, "0xB8F758b3f2016Bb391fb18C7EF39847ef164"
                     "649e")}

    def check_gen(self, Coin):
        """Does nothing as gen validation is checked in the base class."""

    def check_load(self, Coin, wif_str, view_str, addr_str, wif, view, addr):
        """Load Coin from various keys and check incorrectness."""

        if Coin.has_priv_csum:
            with self.assertRaises(coins.InvalidCoinError):
                c1 = Coin(key=wif)

        if Coin.has_addr_csum:
            with self.assertRaises(coins.InvalidCoinError):
                c2 = Coin(key=addr)

        if Coin.has_view_csum and Coin.has_privacy:
            with self.assertRaises(coins.InvalidCoinError):
                c3 = Coin(key=view)


example_keys = {
    "bitcoin": ("KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU",
                None, "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"),
    "zcash": ("Kx62UU7eJP4rCtaU1N8zy34cWnkj2CoFfPbetMbSD9hoY1gDLvdL",
              None, "t1WCf2xoYaeUzHKjdLCxjHL2c4W2S6jZMSQ"),
    "ethereum": ("ab2aeb09578892b1658ee824ae166772c57ce4b77685eca3ea6647da84b9"
                 "6287", None, "0xB8F758b3f2016Bb391fb18C7Ef39847ef164649e"),
    "2give": ("6d27VfDMQm9geZhRjkQiLiRKqW2xXtgqAeNVc2sW91fn5dSQ524",
              None, "Gyphwhw2JGCKhuXRPCMv6NpGyBqBF5hwhU"),
    "42coin": ("5Zo2WUhZWbSENAEhphFRnvinsQedxudLwohd9HWjtZANLpHAkKj",
               None, "4JS9AAQNvG2RfRoRU5vgu78JcvbSm2b3sv"),
    "acoin": ("8j7hg3o21UQVHYgiyaEixB7q6JrMszr3GoT358vPwFxypVEmUTH",
              None, "AMSz9Z81BHYo9bdW2Um28HVc5nWbz7gVHw"),
    "alphacoin": ("84X67qu9z5kbxQi5SrrcVz49kiZ5bfkMJCyiMuRkZsB7wBjZbcM",
                  None, "a2uXxC2DVyFcgoy6r1zoZK2saR61rPMcGE"),
    "alqo": ("7V4gPQgRDTLfJjhZdqYX5QqUtwt4xNND6BqrG8n6f77vVHZ739b",
             None, "ARMFFqgVuQduhtr6dZYhuENRrFh5dpgR2Z"),
    "animecoin": ("65HLraZgUB1ZMqzbCw6pUcoSANAc5hFJBu9wkA38PQbpie5ETnk",
                  None, "AGSLybyLQwGLUQmM2zFRVtvKscCBe2tSta"),
    "anoncoin": ("64o7KHEnsUM8V3PyvY1oxZnwVws7WLD4uzDRj1neRDYrxfdN8bN",
                 None, "AeAbUQ7SMkn4sg9dpp1XucsGzcVbYfLBA8"),
    "apexcoin": ("65FdkKkMjWTmDEPNEJWADvz43ykoD5GgvsiXZLRcBUfFLbbgfkG",
                 None, "ASrYp42vHo2SprQJ7N4pPXSQS3SJxexaua"),
    "auroracoin": ("65XLJaGafJM7s7L6uppX2nYWtbGAYCtgyfXw8YVYH7cQWddmaHG",
                   None, "AHukdaAU6gNLByUYkRfRT9bqe3X75ZdfDB"),
    "aquariuscoin": ("66AGGwyDR6M7AuhdRjrJWDngPiBWZXMeFUiPFZTmpWrFCGcY5UF",
                     None, "ASSYgZpyN5ryjFGsiH6g6dyYCFuPubf38b"),
    "bbqcoin": ("89TVaRAfyauPNPz5hf1JBF91zMkaXSqtxiAZTEvQWLxzuEdrjyK",
                None, "bRAnds29iKzVkPFM3mGnqjLLhiRbSYpyct"),
    "biblepay": ("77QGM6fartbjW7PmfL9bKgboD15Tt7uYy48j3KXHVZmYXf5CqnN",
                 None, "BLcu5ntKGgAojJE2ppeToEcrTVksaQwS2o"),
    "bitcoincash": ("5HxCxKsqC9YsZS4wjGhbfEgQdvpk7w7Dkkk6Kn6FuYPm6R46V4D",
                    None, "1C9BpHzBytvTfsZgqyTFDhtciVVF5Gfzdq"),
    "bitcoindark": ("7KyKVhmMz8cd3eHGcvFimQmXWGL1Kn5N4YBJWkCFU3JhxSCmz65",
                    None, "RL31K4gQRLUTW7VfP1ZKNUxbQAKSHofi1t"),
    "bitcoingold": ("5JDXDHoqaHBAoVNqseLBeWVEy2QczeRjp7o8MZpxFiYdzN5SEL9",
                    None, "GZdDMRJbm8seTp4ehXkmuPdpWE6sWAfEFq"),
    "bitconnect": ("5tvZrkcwhw58fKu8QjnSUwCXWD57jmTGXeNYv5SyPeTyEtnGgEn",
                   None, "8LqZhj6eZv6ehWCGDLt4LUKt2QrYz4JL2g"),
    "birdcoin": ("6sWAEnzkjhqu7ajARwYNNfRRymShWGJHEQcCFRKfkrNpebxRisA",
                 None, "L9rm5AondGkqvEDRqDvsrxVmt67KkwQjSr"),
    "bitsynq": ("7QrdaDuDnuXa74vwiELHU4uPAZ9Qhep334uscnyqWM1nkXTytqU",
                None, "SQ6csZc4eufqdkEf6mA7yThEtDfwufztaU"),
    "bitzeny": ("5J2BWEFpxphia482XQK5Fv9ycuuUH6QjwqrMmHq9sMQ7RmFMEVG",
                None, "Zh1rNqeTr2fj6TKmZT9yJKZnMDtyBqAepy"),
    "blackcoin": ("68ZtpVKVHqKVojPm2t1rz3aFNBmLDUw7eHseVpq2ady6wzRcgUg",
                  None, "B6ohRfAntrxkwqwmnKsCZBCmojhQk7xmhy"),
    "blackjack": ("62Tqa3BgThR3VxBGhUMJkLkCfcPt39imRJY8YRXsPUaNVj7YGtj",
                  None, "9qoWkfqMmNL1YzcU3bsaGH5DR1StJJmtmc"),
    "blocknet": ("6BXC6mcEF7YnmifzxkEVWJZ7E96o2RkxCJjTYgw2dBsUMDrNE8e",
                 None, "Bmbx4BzDK73ZNe7LzYVYF379BSNtWDgkF5"),
    "bolivarcoin": ("89DB1GU3ypSf1Y4UKo1AxByuffAvFkVH57GifbSJFSWDobKbsRK",
                    None, "bGvwkMq6Aki2AyWyGDM1skRTgPCApQpVci"),
    "boxycoin": ("7podKbhz4jVQHvxTSXHK2kqCXLdFHzdq5kcKCYMAKtBsmSDvwZe",
                 None, "XLtToL4TVBjoDGBgC7Gr2btGJfcETuNjWQ"),
    "bunnycoin": ("6Am2fzQYqjymmgHcXtdVQHemDCkZoijrdSZc9feRVWzbXDNCHEu",
                  None, "BVTvWNCSayMLupnDM1dXbmHRvQhvjnH7X3"),
    "cagecoin": ("6Lmwrx8PsjVWfKSb9KsKX4Lt23kEAXqhf7KqfS2UAkU2Kn5oFVZ",
                 None, "DXr9M1M8xfZXDdS2R1mbqToGAadDBn6Zji"),
    "canadaecoin": ("6EMTFZxecuxYd6iWkQjMPwTk3pmhkVRL1ydUSFUYDNCHcxZAfTv",
                    None, "CQatiL8pEpwBsdpiPuuLY4nNBS4griMjTB"),
    "cannabiscoin": ("6Febn8qomBdLCKZHAmQhfauswPSQKD4s1ZG2JMhFTYURi8peFCR",
                     None, "CRvHJRqhttcSjZurtGQVNcKqVxaubPL8YP"),
    "capricoin": ("6G9FAYbpXSg8rgj92DAodMEGvJy9brukvj5zCS4oRz436b5Yqaw",
                  None, "CJyUMtvG98ejxtPhrwJncobekeUJBYge78"),
    "cassubiandetk": ("6KKvwKNkwwzeEzArv8vdd6vDmX4o9oYVy3L5oNiJLA29tC5n6ke",
                      None, "DTSZk4b4HZZDXWr5iJNx4VqTFFyyDJL6m3"),
    "cashcoin": ("6TU4WpkbTE3r8siFB21XsAda4vVEZx9jEYCrQbr9PFeXp6W7M6q",
                 None, "EsoL2CVBwoZZ6gAGuV6Jpvxdxv9DjAPzpc"),
    "catcoin": ("5zfRfm5JMuJy8sSxfkibmbbWGadMbqfomvATyYq3hYbbngGxnM1",
                None, "9ZKNR5gNDKRZQVpm6fmkAppaxzcxhRCafF"),
    "chaincoin": ("6EenU6F3azXPQdAAKaUh3QPrEos7JkCTeivL6bYwy8HwP6UPaFk",
                  None, "CNDMVy2QqMZRc46YpkkA63JWHiJTtmTvnL"),
    "colossuscoinxt": ("8843Eo7NjpJquZ5oDXh5ZwRkckBzY846F3hXJ8BB1Sga9DJAwAb",
                       None, "DBYG1ewefJC9Kuk3dcfJ5PbR3T5gt3bgmk"),
    "condensate": ("7JarMcTBwZdbLKjXojJ5ueTPeYzGfEUHP72EYsErRZw1ijT83oo",
                   None, "RYUeu9736NLBUDbzWigGhQDAHDzJDwg7kt"),
    "copico": ("5rFk3jqmdptCMGCa7q6uizkQNhfSWQmfP31imkMtoibRRYUPj9z",
               None, "CYShSJjwV4JxqnoLC59jpSjmfnd37Ju4fN"),
    "corgicoin": ("6EcaGWNgMqYyZxvhLR3VfyLoQ9qAfPVdr7S1YDT66N7iNyhjX5B",
                  None, "CUdcVgAFUwrc5EMGu3x78Zgda8hCSknq1Q"),
    "cryptobullion": ("5gxCwcHfwBVDoVH9PjamTpbWtehLGAsAck3cTjpUUKDtyW35f4Q",
                      None, "5gAyv7L7xkvAWvtZoAoWi4R4phR15L3HVv"),
    "cryptoclub": ("6UsGTEVerc6usFfxXAHNoYasfa6uL7yJLTLtURBJZeJcr8CUrgv",
                   None, "F8E9VGTXL98G8ak8o4PQHpjoMk3DqTWiHK"),
    "cryptoescudo": ("6EzrpePhtfHuRHo6CJHzAkmYSzrPKB46oMxvReZJYb4MXMC7Xci",
                     None, "CJo4L8DoSy9CtYYqdEzFio9pjGyvc8Q1ZN"),
    "cryptonite": ("5KhqBuUx3D5HgYKettG2vSDQXqZ88mven1X1WHkDqJvsFMmhcUZ",
                   None, "CejRuo8nCWSddjGt9SQUKGEY9Yr6SgybD2"),
    "cryptowisdomcoin": ("5Xmx7RNFaLzeED2pPx6FwaexYC7sxyQKzZAwzA73ddFPDE2Ndi7",
                         None, "WkXiEa7kydQd2TBdVEnMRRpLAFiiPB36Rd"),
    "c2coin": ("6EmJKx9yWG7h7PfUTVjvQ6KzM2Jijd3UrjBHwdSKFNKFdrUqYQ5",
               None, "CUz7BUJ3PrJbzeHRfi9NVMFHDv26pJLCjT"),
    "dash": ("7qgZGm31ShqrVgkEyaRsNdLvKXCDd2MAvAaEa48fXiAQvwX8Kkk",
             None, "Xdp48vgvhm2zVkVxGZECw5uruPz8vCtdc1"),
    "deafdollars": ("6viFRNLjPeFwDxcUtFR8DKPASGYGfKNrNvWxEb5RLhPWQYd8qvn",
                    None, "LL69b2a2ueNzJ5PHweLdCgZ6MmJAu8YLnc"),
    "deeponion": ("6LHxwwLqEiVAryWA6LDr1hedGUsiawBf143a9o57ZcABXuCUwCc",
                  None, "DjLu96DtbEpMzBYoU1RfQ649RBcgGDn2op"),
    "deutscheemark": ("74uSy6zNaBfbk4YXy2hB6jEXEtdLBnzFVepZt5eDcB7Qy2hKJhm",
                      None, "NTWc3M5mX54KTwqpoQr73g39eUtVNwu8yi"),
    "devcoin": ("5JsT4rmZYibwX4VV9DmUdrurEvRUuJgyP9pU19HcySiYJqJZgtZ",
                None, "16T7YBYfkrZkErA8wyBfRUbK7x7BxJUJ91"),
    "digibyte": ("6KNfkwUH54s2GUR12MnUWy1cFzYDrZxrmuKATuSWkEL6cz9vJmk",
                 None, "DFH7BSp1reF2uqb44sr4BCzgvYrCvE4Voo"),
    "digitalcoin": ("6JLg3yiMBHdQo12awM4NnDTVgKRRHrS4vsPV4gjibaetHZXLkSX",
                    None, "DGccKGGjqfMiEzCXm7t8sDERkpst1dTekY"),
    "dnotes": ("6MdMddNCqoMa7uwRYBoW835nVJzVSu415tUcbCkhuvZ75pW8Lsa",
               None, "DsJcNskFgaJ9knkgzCGcEVdPtyu1qSKjQy"),
    "dogecoin": ("6Jsvmpaz6BD5YwJbKgM2GdCFZzyiQrK3MizpvaSyBYp31ehthH6",
                 None, "DJFfX46Gd2BjeWFJCc61YTpboWD7sbkLYG"),
    "dogecoindark": ("6JVEAPPePWUXy4DnCxs5v39PkivHcpJH8NdgshkVyBjJ5n2cG2t",
                     None, "DBA3Pr9SvMuSZpVXhbHK37EeNdV4y8ohoA"),
    "egulden": ("6uhv7NURYfHfG6hgNzNZgehPD46ErCraZwgJX9BCZya6ZV8PkMz",
                None, "LTZ6jW6xfG9uVcoPttXd4nYmYBfnuYuwav"),
    "ekrona": ("6on7mbGmX1qiTLyj263xgthUbQEXLYPq6puM3M6d7fZ3FB526p7",
               None, "KUviyC2FNGXvAAFEsxkidpAzGdBDnsxViP"),
    "electra": ("6RZGZpQPR5J87XJDGv3w9mrp3BuFqzsJ8sZ763m2ENSK2KPeucs",
                None, "EQgJtdpKiQgapbyVbXkzqiVYbmUym7KQ2q"),
    "emerald": ("6SeQnqMs8BRXJNEWqW8Lixm84fWHbjnEf25UJVWiiNCujKUAqG9",
                None, "EpbgaxAzEucrV3bQ59WQrGVgfFUvS3pSkx"),
    "emercoin": ("5Kfku7VVoXxmZycYKCHnmr5Cv99654Pwhp4d5AAky2NDtxXU2KM",
                 None, "EbVDWbqQcZiB7NYexddWgzDB5Aa4mP5pUv"),
    "energycoin": ("8NmeskkSBLGroyKjTkkWrfCGW7cJmVstuPLr8SYs9kABJ5kXNXa",
                   None, "e9ZcWgYRmPai4DzP2aP6n1ZgpTgpHTiYu1"),
    "espers": ("6QdfA6mo3VP1NKbk1A7JSf6BSdAtZSrSE1e6n8wv6jm4JnQzTaT",
               None, "Eb1p3Fy1aPgAmyveBmuk1TfgGTaFYaQynz"),
    "fastcoin": ("8Y8MAyJFDrd4k3kwEBU4n2txFaWivY2EwFk85U8KFkmk9f9AJzb",
                 None, "fwxxreHBiTSjN1uZzvaZraAchSezLuJgJB"),
    "feathercoin": ("5nGxEhguk4o5qDQ1rq9XnTNjpoTnXPDsdwzQZjRh6Cd8PqH6YbQ",
                    None, "6dnAcGn8t3Ea4yAC3zuYyBqSjVoqXALdDg"),
    "fedoracoin": ("5JRENpx3ozY72rYRfJG4wviP8BiDLkGmM7hojyLLtr8MAy8xwaV",
                   None, "EdgEA65MhsdjShrmQVSryG3kV7AVWAKT6V"),
    "fibre": ("6Uv73YtvBUnwBJQLP1LpB7qhhvUk6oeTXndeE3H1oPgwZjuGzAJ",
              None, "FCppNZNfxoE1YEtcBpV9hKqaFJ8QQFivFE"),
    "florincoin": ("6vL3ugPAW96VaAQmzDo9g3U32G4bxBwekTsy8RQPLBhfJPd4uim",
                   None, "FJpVG3gPTLMgkQAav6PtJwve6DHo1cHgrz"),
    "flurbo": ("2cNLJ8dGsptsmRy3SxamEi2U1GQy7eURpM9L7fgf9ywew8gaH6x",
               None, "FNiBHF2d9Ra4JwLXLE528RPBLRUz99R69A"),
    "fluttercoin": ("6URkVnsZ2wckfPUopKjirwjbhpczqhxi1648HbXnGivTjvM7g9s",
                    None, "FTbYThLHCufCp7wMkpMzkQ66h7Lk3fjhe6"),
    "frazcoin": ("6UYp1g69aEzZNnw7B1iHMnSndf5r8kXyrBF9LJXmoX5o5dN4t8s",
                 None, "FH7XtRXY19iBsZcPzh6kKoK2fMXPJtEFcZ"),
    "freicoin": ("5JNrvveSqEacVugHjV3LoMXT8FXFA8ycwRZG97w4GcLKrMF8gbA",
                 None, "1EYcmXbsYHkWkjZQEY9VPj7GhWnMUjva8M"),
    "fudcoin": ("6TyzWE6gg34v4jHbe2Q1aKnfcEQihWQNzNaALNw1GaqdKMrJyrP",
                None, "FNid79aFyVaqNt8WhL2wwV9BSKghEhBv2J"),
    "fuelcoin": ("5Huv3AwWQn6BMpoMsuT4kFJKb2gPi6s9D3eLxmJ5q88Lb5ikfgb",
                 None, "FsM4wtrh7fnwKoXAq6sa5k6JitU7fWYWaY"),
    "fujicoin": ("6XWeFP7R6ZvHHkpzbxUqE4C6J4aAgh4NhBFhbSm28yasZGjoDYs",
                 None, "FYWcTZTHtuBscerPDoxmwP7FPTD3pWrtsQ"),
    "gabencoin": ("5qguGx7DbWSjNzQcehyRVMyxVyPjvKH7ySqb5vsFba5AYCrbgMi",
                  None, "7mz8ajyatzMkuStE8WDZ4RFNMi1vdUT179"),
    "globalboost": ("6aHEjnkhnKAuEdnGff6cxVJmiNvxAy9QXDwHF7oTc1Xjd1sF8Y1",
                    None, "GUedMpB2Ls52aTh4S51v3qJ8gHqBMkb7R1"),
    "goodcoin": ("6bayethSHAp4Jc2iEUcL3vGv2RF4iJZfWvKqVXig7U8XYjKxp4Y",
                 None, "GXMRmCzfyJVVVJvv3kT3LGyxVxA6WWdvC6"),
    "gridcoinresearch": ("7PuMzYZUGQ2q79SnoEuCXW5io4UvqgLWARWzCQC3BM5HbqzEGmY",
                         None, "S32qqtxmySFzBXjiTXCpAef3jkKrFwat9d"),
    "gulden": ("6a24i6PvAX7GAx17S5BDbcd175RdKrvKyPZtp6mm2WC96HqcfYJ",
               None, "GY9pQcrqd3WZsoTmvTST63L8HNqWN3WduZ"),
    "guncoin": ("6buNCQCt7ioHhJyay2PZmh67JViCgfPJastYLX779X5kA54YRCa",
                None, "GmZtdjNBCEU9KaDMi2SWY4rHwJ5McwovDs"),
    "hamradiocoin": ("5JZBFBGzUi3D7nvLGMUrLpcLDB1YTCUADEwSFipY1ht69CxwSJk",
                     None, "144YrmoUTY1Joo6MV3UV6E47E5FaJ7QsEd"),
    "hodlcoin": ("6f7AY1SvuHu6RQrggh14kTEdkeUGME6wocPBp3VqvGfriFhViTY",
                 None, "H7q1UwY6QhRLAVv616DxPsBsSvySfGCzST"),
    "htmlcoin": ("6fkpWySK3zUDagaki76RxYbhjNKnPMq13x6j6oTijpFXtg9GX8U",
                 None, "HfCA72j4sq89Wjj7RZcfxiqDn3oFN4ygPU"),
    "hyperstake": ("9F2PhNEmFtLzGLjws4x9cYSD4hq54pBbH3TctAHoCC7cAhe8zGR",
                   None, "p5zTdMsbmVTdJ22cZB2V2d7f3Fbo6kk76p"),
    "imperiumcoin": ("6vkiHFo5YBY2jhKqHRsJyxN4bb7jCAqAVGmhWtCFeSLaZWoGvU1",
                     None, "LN6PehVsAZUF9yt4t1VjsU7Y5LSyTdYTED"),
    "incakoin": ("75bV177WmTd7nhRaEaNY7h4RPTqgaL7hv9Lg83M8UvryWD3Qtks",
                 None, "NPiHTgxbpkRn59cU8v3tfutWmoSfaaN41e"),
    "incognitocoin": ("5J6qke6HxYobsDp3CnnqRmo6AgZnJ5pJnKRBKv4knisU1iHsx6d",
                      None, "17yAi5kU5JuJH4qt3cTZVtyzXKUgUfVasH"),
    "influxcoin": ("8iWhc7zyYtu9BA6ojB4BiyJDSaHNqZv4eWhDfwC6dpU78SbkdtH",
                   None, "iAHK5iief4ReJCwzfLD9HuHWdZB9kXnTP3"),
    "innox": ("7ok85muNNEzHwna46Nfi1PxgFwxAKKaBw2AvJwCU7TrhXHGsj2t",
              None, "XL2uuYcLm2PyKV3NQYaYikfA8E6Nqmf8Ru"),
    "iridiumcoin": ("6vgDdHR7ZgpPBgLBHnsJnFvDePcBwTfU5jeFihZJAKZkZvizTfJ",
                    None, "Le8gSZU3dKzhsAjDppDWw3swh3PWC7AM2r"),
    "icash": ("7rhiRZoVHUhLHrVCxnKLMPQHVpVmBXC8NnDKbxrCQ7MbESnue2g",
              None, "iQThf9P2wUFTQ6snBigpRwsXwx9iP9fX5S"),
    "ixcoin": ("5KDHdXwNr5uDYL7knzS5zJut97XDwUBxysSFxMY128Qo5EA9mvU",
               None, "xbDYCqxK6fb7ZwXZsRtSQxB2FWSw2fNB84"),
    "judgecoin": ("6kKFo3qWSXx8UQTMJhNXV3DMohYAH1yWQeBnkZ8wYbpMZBeboUM",
                  None, "JSNkGFnGR4dwriRArdi11MDab1a9kkJc1Z"),
    "jumbucks": ("6jS6XEnDNc9JxRHpdxEJ4bpTAL8QmgcBnfds285bHQd566PcwoZ",
                 None, "JQRGizJe4PuvNxr6RHkg2QVNx5J1wUKsGi"),
    "khcoin": ("6u91S3rcXjcf4sWo2HCR5oE8pLeDy7sqffr2oaCVjfMm64snaaS",
               None, "LW6G15EzuiiETxPsrHQa1uNhgrq3fuQR6u"),
    "lanacoin": ("6uuf4bAB6qqCJop8WCboA4c2UzjV1h2Zit4Am8ZnoXVBjY15ExY",
                 None, "LgbvBxMRSabaPaN4DVrGyu651op73nirtr"),
    "latium": ("5Jm3zJJkE6aoZRMtc6kBU2yrtcWFFz6Vcnwg74e1rcDo4rzKHWu",
               None, "AQ5KuuJcUCfWhHJ4eEgVDhKjUyZrLFo1EC"),
    "litecoin": ("6uEyVoyakFvPUGWqGB7HhYwHdPVAB228XEGmqr3JCdn8wXJhtnt",
                 None, "LbwXaBYdox1h74kJ1u72YFz5K9jhnnvkZ8"),
    "litedoge": ("6mC3CBaStpj1wBdi1a67tWU2tb1GeHx1yXWxhKdHsSZEPHtQq6S",
                 None, "dWm4u2f7dK6YSjZMRH4cgovzi5NEv6HCHu"),
    "lomocoin": ("6uxR1EZMBZy9AEg3xFVkzi2xRrQe3DkacsRtyY7tsTbxNpHnNyu",
                 None, "LafCq93w8B1wDACLbTaJtqoJBvK67rLmU5"),
    "madbytecoin": ("4haefwUHRn36KSLFxdPvBgzsdx4hJi5tvbfUD8MNBr85JkHPBdf",
                    None, "MLudb8ug1kGNvQjWfdpAvSBPuvW6wGVbdY"),
    "magicinternetmoney": ("6ugnoDxEjQJaEC6a8pdMKRovCWd967C2hD9wWiygnHbjYt59P1"
                           "z", None, "Lao7XjuMNGbVbLdbXjmCR9avvAAwzjpBzB"),
    "magicoin": ("5zVicCUcWHrhSJy542XpqLY3PS6Qmsn8py8UpWNn31WnGQicF69",
                 None, "9RR4otEpj8Go8k5DPJqw6CFFcyAidps3XT"),
    "marscoin": ("6yNee8w56CbKVyNrDJr6Dr4B53Cgud29UCNvPvcdRh6b8774VqG",
                 None, "MT1oxf7ZJdj8TeoKg9VzVraowp8iPtuiiY"),
    "martexcoin": ("6ysjx9PMZrsjocJkVJjPWwbaLM34xdX7XiYKSf85DdTc4Xyxrv2",
                   None, "MCGZ2mvdkEPk4GvGi1BBfvmf4Cp7pa6uyr"),
    "masterdoge": ("5gQCcEfYwVRyfaHUZjDk1K1AzdeYSrm4MJjLGFShGWAesAHgbQP",
                   None, "Ms5oPeD8ATqAvmtRKYg8FxwMWhpbtNmXPk"),
    "mazacoin": ("8XaSnMFa9M9nXFGyxmxX1h8StrdJNK3gwzwp4swyr746BU2zdLV",
                 None, "MVg6qx7TgZJBFzyMQcryMpqwSE6zFX1NPU"),
    "megacoin": ("6zPcfj5coMzvdBAswssyH5UN5AwPyjEWTwUGtEM4LtxahmPouqP",
                 None, "MXC9vMJ7GJVfZfJyy1pWpY8NUn95qqJuPh"),
    "mintcoin": ("71cvDGWSd9RTRKXp5FhcP5khc8Viy7NYoktFUeYEamciZb2fe4h",
                 None, "MtLaLtxvMbuLswtMtuy7odfzkRo1ePuYFV"),
    "mobiuscoin": ("5J2gBvDwsCSPPqqZ8HqMMdgHJYH4sWp4tn4AoUDjnsfbdDbMUYG",
                   None, "19DJ4zkvwDGBG3MPKACa3hmGb6Ax6bCpMG"),
    "monetaryunit": ("5FDVWAxZxXdFLxPB38ZqUuG7dwmYM5cLNZiprLX7GTLXJBwan94",
                     None, "7piGfuFPmpN9MqeZNCbC1rSDLbhmURzsrs"),
    "monocle": ("6yokML1HYF2sn9rnb69UwRKXzH4AhyZ7Mqu9nkmWaDAdp8PS3PA",
                None, "ML6dMhupnLAu9s25PuH9bGToQ9cAx4LQ3Y"),
    "mooncoin": ("5Qjk3cHg62zUfLy13paCkT4UyLGYRtLHPSiAoqxBjAAenjvTgfx",
                 None, "2Fi18SUmHV8PRtZ3siFaKB687qZxMJTdDy"),
    "myriadcoin": ("6zmXEzbK56dzVMBGyGDYyrniMNpMzRA9unYLYBtMFHLcyfP6AKG",
                   None, "MJ5jKE9c4h7vW6TY4UzyyGr1R64oQAgjRE"),
    # "namecoin": ("5K6SHE4MzgpHFuEFVmm9gG9SHYLbCNcQRNJXv1HkuDs2SnfqumF",
    #              None, "NDd1ufHRcnARAqX5vXSc9enJVwCBZd6dzc"),
    "navcoin": ("62n3gBU9ae5mPUohY1jMVffEvoYc25yZL35AGYmYmcdE15pKFQM",
                None, "NgKr9p1q1HbVbV3pT3SDpRVHb5awSepkhY"),
    "needlecoin": ("76BMNNn4uRVdsrtbQGqrWxdrBiKTpWSF8nXnZjkDnJCo4s2Ejs4",
                   None, "NVcutkZniGmQT1VQKq5BGkV4C7DXj8SNpN"),
    "neoscoin": ("6xr3rifVLTSFYtJCRcdfqrqdjQweev54jpRC5RAxBRAeEZzAYvd",
                 None, "NTytSeojgkmwf1FTDa83G5BTK9oofBQpph"),
    "nevacoin": ("6whxHqeTqQ3fcCzRBBB5FWH2hmqfKmMyGinX8bz895u3uRSzpxZ",
                 None, "NaABUuBfo5mst7vNkrtZcA95sQvTNtRp8R"),
    "novacoin": ("5ak5NSNFZ8fyN2AwPCgkAx7NepUgkoy4QfDGkQqj4TsEWvvZrce",
                 None, "4KMJDgUyjM6W7NqBHtj7PA2fYBPgzgvAyJ"),
    "nubits": ("7RoDpCN4d7sTQdCPPj7VMc6sx23B6RAUtFb8TYR8PCzGVk2g46K",
               None, "BAfAqkDTs9hLdhtvtoYnUsmRBgGwFV1Gdi"),
    # "nyancoin": ("6osRNjuhsP8X1prcZwt1tdpAvHwGc3nW5tycCFFqnfjQw1QcYoE",
    #              None, "KGragZ56vy3HniJEctaHUa4zUGq3UGPxv5"),
    "ocupy": ("9AT9qtcNtqmx67LJ7f5gccwSpawTnXt7xbjYDtXjjKASRzLWWq3",
              None, "oJwKDoiu2cg1UDrM8TTAwwSUaBQet5ssjC"),
    "omnicoin": ("9B5HTRXcExEvU3n1d567SWUARiZVWxiCD1iK73BYaL3b5bbXxwH",
                 None, "oQrSSDBdwjdAXKfgK9nGwV2pkkJZk5kPRV"),
    "onyxcoin": ("9AMzr1uv87ko12G6zbSLBUzbfHFtW4RsENcFa7AVkeUzGRpQtWS",
                 None, "oeXmuHdroz2gj9HNyAYmdQaBTRQMzWGXLP"),
    "particl": ("4dsLuqWfSwvKqniTSDU6AFDrM8pUrDPzYWEhAMq38oGZbJX4qLk",
                None, "PXwfZAwurVj9w1PrWceiGPyHdHonNkhxqC"),
    "paycoin": ("792Q5GVSndkTv6yETtdUiqkEhDhc6P6ENTaNBST2SB9mXqG74qk",
                None, "PSiX53H1ivCuTwJJ8ZuNXJykbCqFnENscE"),
    "pandacoin": ("79arfL7ie5ztqvavCVL3W2hvQrhDAN1eyYWFz4rXJzN9RCACQ9i",
                  None, "PUTijk9WfbekaQujYbdrSvL77duUqV2CZC"),
    "parkbyte": ("78ue6bsyrXDvWf2eZurjZdaussXpmMRYcUHFXJQ6UFSTq4G4o23",
                 None, "PUYKqgqLFbs5SbdFPUj4r1kTyLGUE59SLR"),
    "pesetacoin": ("6sTFbBqEQUvxVLetLe68payGWrhJUJBRvYj3U1WDEMPzJkKZfoC",
                   None, "LDUVPtQTogFgMKoZH7wKADQLU22XqpPT9E"),
    "phcoin": ("7AYQrTfPgr4o7a7VfyLE94CurpLVDeK4HzvfqQAEn2XcohVYiLs",
               None, "PPDBQpqLg8K11p2qRexAiB5XwEAqvayyf6"),
    "phoenixcoin": ("7CSUdppPpRv5L1F51xLoVuyj6j9M4qXRkY1NHVaP36izQch5SEt",
                    None, "PbgWRg4hUgww1XFGcpLn8HU7wo9oUNVt3j"),
    "pinkcoin": ("5PmKMPirRnH52bSUY9nfXGztGWoGsBDgva67sryLgkZJtRaa9Ky",
                 None, "2QWegqeA4q7WynWeJtBrF59BoCvkmWE84v"),
    "pivx": ("883m4tus1c6XpLgoS9iuRPFrdPtKmJyR79v6zAiwZRZsWAj9PUA",
             None, "D7bRjDKx1YctaMCPv9Rno31iTFuNvf8XbQ"),
    "peercoin": ("7A4T8Pqr91ZyKNedrPAuwWi9V9CX1MhxbBHmUtGncPdpwxnTDu7",
                 None, "PKc1xLBWwgchbu89oak8MKtGcnf4k7X2JK"),
    "potcoin": ("78yRqPWfaQHp1SRyff5a84CXFtKMoRYsmoMzW1krCqpG73sfEq5",
                None, "PAfN9mTnoWbrreeZ5zHRS7VynKGbcshdKC"),
    "primecoin": ("65rP4gSkmWvqucJRKY6eXQJhJjgvUwiHC4RxrPgRbdbzeJrEs9N",
                  None, "AaAjnPnSeC8tDYi2sEU8Uzuf5ZEQHJ2nXs"),
    "prospercoinclassic": ("7G3hZdZL7hhJhDAtWfWJAcJtAQhLZW1YM14Ym9zteHwYAPYtnE"
                           "N", None, "QVYHqChVMSFUPabHgekQ2LH5H3P6o7azQV"),
    "quark": ("7EmdKWV22qRsPUMzpLcHPaYUQs7A4RYfHQLRzz2C5nhaaK9pb2v",
              None, "QiusqGYdU2jnJ1MDe9XxUXLrrqjivw5FXr"),
    "qubitcoin": ("8Wej9kFs7zp2K7FFWsx6fGEkcjsNC91SiHa1zGkQeiU2uTAZ81N",
                  None, "GUN1L4j5d2Wgqsa8sN4jw8u9QHrjx1Wp78"),
    "reddcoin": ("7MB6FDK3UG6YxQMwF7c7vFwTx6P8oAjeFDcvYASFYcvQxbtq9nj",
                 None, "RsumNHuVuzhFMhMavbM1sD1bzVnByJYg8c"),
    "riecoin": ("5JW36qpTKSNREn44z67S6iEk16za96oPBCU5B6ockc1mMmuzX3V",
                None, "RUangL1yF9f274EhEyzzJLxCDUCQfMGSw6"),
    "rimbit": ("7Kyas9N3tRhu5x8rmnTGiZFB1eDvvykofodTg3djZauzWqn6Ujj",
               None, "RPFCYEnLuRq34EZ3cGBcnMSpZdaDe1ghYR"),
    "roicoin": ("5JUDTqmuLGBRTrWYrAgd7GoVTz17j8d7nnt19A8SxsHGRBx8oZG",
                None, "RUyTQX1Yivd7WFYRd8qB5WsRe2ghU6txQL"),
    "rubycoin": ("7JVN1EP33knecbnWrpmM99jDabvR6WFTcV8tTToZNBWtx2nS8JJ",
                 None, "RW8FhCfPgNDywazzXnWe4uzsJjvP1xpBAv"),
    "rupaya": ("7LGCG3nyP3jEDSPL7ETXsYUEBhq3zuK9h3CwApKw3pqC49EMqBB",
               None, "RBgfs8eGU2rxPHeseZNUMcEDLjBuVVhdTp"),
    "sambacoin": ("7Poh24Y9Dv5uqu9MQsiDUuFV3feUeiMGbENr4AhbohkTnh3qsUD",
                  None, "RxSRNfNEik9ok9STa31HJ5hn984hDNjLcs"),
    "seckcoin": ("7RAKwDZpg1Crng24CfGxJn2g1umXsfCX2ZTLHwXCLV7wa2bESeL",
                 None, "SYTXZqaysKcANLCPD7ZDygMKjapzmJ2QNk"),
    "sibcoin": ("5K9yBMNsECz4sLYzdJUCXzRs26HgiSkz8MLu8eu9amnyiRBX37C",
                None, "SaJYV4hXEjqk9Ew8Q7AVhLeonwn2pEhXNM"),
    "sixeleven": ("5K4XVo1PDVQV6jRSUGEFFFXDhratxCyQmArXPZ1x1dGrAbdKhy5",
                  None, "N8q6KqGikutaHJcHb2hr1GX2EhkvPZx9Ck"),
    "smileycoin": ("6ABZCDyaRXVvjwbwT3TEHxp78F38UBpjnkwf9LAXvLK3zaXE4aC",
                   None, "B7ofjeX3cRXVTPfQMaDpxh9HHd2xheyUPn"),
    "songcoin": ("7R9Q7LVeZgEvjQYCwgHzy6ZVxF9ZShAWVYUzoKepoeZtwjmj8oH",
                 None, "SZgRUUJqyoeNcFytHP6DyQj6sKkfXPw97W"),
    "spreadcoin": ("7Qxud8Gm9tyi4oJedKgB2S27urFHnhKxiWEtcuijnMsoUzpqbqs",
                   None, "SaG3ZsJK9VQeX8RWxp6VCzSzebxkZJSmRf"),
    "stealthcoin": ("7PrsnVozsVQ8uTPmWigxxiw21RVRzE1eZm8J3jWYAVCwGgMNgBN",
                    None, "S2T6BYGTxTeTKJc9tAws84RTx8egbteF1v"),
    "stratis": ("7QTEButYaSMFuem7x4AxzykMbKPiaE6oHqgPQpKvd3nM5jnmA4W",
                None, "SfC5ft5RGJWUtccjBRGsiy5L5Pd57vYtmm"),
    "swagbucks": ("699CJTeUi3oMM2JLYaUFKK3s54ECL4UcNvd8rJU23ij62VPFktF",
                  None, "Sg1mcQdqP7U5wPt8BPVBR4m7AQCsXDeAmY"),
    "syscoin": ("5Kibvd7kV848Fu8XLvdvuDZpYjMVqXVQWAYhsXwp5tyZ5p8AHez",
                None, "1CUAYsqPB5AEetCYDE4w6wUtgNy3oRgWXg"),
    "tajcoin": ("4ja3PHde1MgbnqpvJKDv3WGfZtFhrA9bJm32dvFBDk7gDnVcPhE",
                None, "THcnQ8Gm9yCta8oSTmdcYRSDACWYnr9PUN"),
    "terracoin": ("5Jqkh5NmbXLx8cpF9FoYn1z6m3i7W9vaJaD5NGP8L82SqUiV1XC",
                  None, "16SzPhV7CLBHqDLWtPEd5Lbp5XhFWRGbRk"),
    "titcoin": ("5JKcQDDsSthtnCKJR2oP5PV4AMMWeYvmkRGa6GA6F1kEfxoUCPb",
                None, "1LBTfpbvZ4JWeLJhH2XVC4oWc99xy2fYUG"),
    "tittiecoin": ("7UWbwZ5E7z8xiUR5STBugEHQShRKBiEnbXz5HTkBSd2JcVUWe3j",
                   None, "TYDEDmgu8x6S5pJQ64XapPxLYUyJbwHVjk"),
    "topcoin": ("7WcWT22585gaQqAFtbeDWEFUx9ECfNzKsGVdDpSGhCQHdW9otfE",
                None, "ThZ2gxByUzP2VyWFF8hYwP6VphAPQf5Gp6"),
    "transfercoin": ("69XRsrAPxCBoBxzxDx5ubdtzSk6ceXPnUaQ4AVug49EytcXq9pU",
                     None, "Tth8uJMETA1w5skPQdBtVph7ABhqHptVPe"),
    "treasurehuntcoin": ("6yybYfqx23PNsKPeyRHhUy83eWrHu2iREgAfdWfG5bwydrZgoM9",
                         None, "MQ7BHL4qMngDBhezLgcB8px7RKd5T3NEZE"),
    "trezarcoin": ("7WtAQLmyC8sSTP9FonnSXpSroohyY4Y6RAaHCuKnMqs7eM6uxrT",
                   None, "TfKK6iauDC1m9oPoZ4k7tCey4QBsLhUBsQ"),
    "unobtanium": ("8WnqrirB4Zoxv62imYLb8fZZ8ktgsgi5o2uiAaejHjvH3WLvpfa",
                   None, "uUeQAMeR74nktBUkFU7yjwM6ycmBJXW5sn"),
    "usde": ("6a6AYQkE5LJaXCe4esH6voxEifgDU6J42UjyPTgjLYmsHPbZt98",
             None, "GPeFDJwiavhcmMJxSbezufCdxmLWMiL6Zh"),
    "vcash": ("7fxA7rctgW7znQLgRZWfQDYBnNMEc27HmCXHXMNNmLxzNWM56Li",
              None, "VuVCRkixc18YUBcU2Cv3j7gZw9bCNEE4vp"),
    "versioncoin": ("7eQUTDR3QvenJmdZ41JnvwFNPCE2NqXG9jXdDtuVUik37RqhkVv",
                    None, "VE4Tz6gJ7oG2ihVcZ3524sWae7KsWFUW3X"),
    "vergecoin": ("6JU3JrJV64yzr2e5FKVNuDH7PspJ7ZnFVD8npuDTGwueZmt8L9X",
                  None, "DQSQj6kUst35HgKAef4ez4tFJ9ntAMH9XW"),
    "vertcoin": ("5Jq9R9aCmZsaR3qcuLF6cS3tFoMMyNfo67aHMtzHPUp6xKUNPRB",
                 None, "VpeFxNnLP4XoYHSKnAUV3nqPmZAns45x5d"),
    "viacoin": ("7gd2Wzzwjbu4GKGMswxyt3HsMmX6PED39rNKWxW2HHzfsephJpY",
                None, "VsRqmvPPFNAAe3DdH5ugL5QnTmYwUxDTv1"),
    "vikingcoin": ("3uXgarXkf8c3TqQEpXsopiipZZA1Qx4ihReXEWHaCJvFStcSCeY",
                   None, "VMwekrduz1VcCFEveSaPzG18tL1uMRakMr"),
    "w2coin": ("7kSohxaLgyAcBoSUJcnmtXVGEBpoEZgAwfqo3HtFECAoRcCCv8h",
               None, "Wfdix3vh4HnoQJjm1VKoCdSLVtXeRtZcip"),
    "wacoins": ("7jxzNeyHCThWzVjbxobZ4sermRzB52y76oskm3E5PC86PJbpWaN",
                None, "WZXQcTrn9Q3dgu1qJyJ9cM2f8LbnhL5baU"),
    "wankcoin": ("5JHSG7zU3VHG81QTzpo75Hw9T6atZi8AkDX9kWTK7VnXH4XoVaR",
                 None, "1CTdQCUyv69KYKs2LcdoaAuqbNQUv3FMEG"),
    "wearesatoshicoin": ("65giWFno8cMLuHzVbDJ6LsjE3JpjKCUpctDBA313uxWp1Xdg8nh",
                         None, "wewgEEoNQ7TpPEu9mnJKRJfsDF6XDRn7Ah"),
    "worldcoin": ("7jsowfepS5GVkgurr6TkqrzpTCakngGekPTxSSyNLg8z3nL9Ex5",
                  None, "WWajjwpJ6hRrX6aiHHuCCXV7T7AST1VC4L"),
    "experiencepoints": ("7pAYxACw4pevRiARd1aoMSFNDum2zW8Ke3KGCCtx7Zqu7URJveY",
                         None, "XMwAsShb6NDVzeHEyse98qSQ6ejkgdkQoK"),
    "zetacoin": ("8YB5hato1V1m4DtL8FrMDkpoCmvVghhjZFcYk3mPXmqqbF3WNce",
                 None, "ZJms6esaQ8Q1qmRBCGWFKkiZ8MnJNgzDAF"),
    "bitcointestnet": ("923YcpcJobPv8axUEFxHz94tyLcXCuRsiukWJpvD1mgSQcAnxCz",
                       None, "mzuWj4bzYV5uGE6NmxF43PbSS2cd7GxqYt")
    }
