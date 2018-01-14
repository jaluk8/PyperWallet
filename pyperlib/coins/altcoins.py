from pyperlib import coins, data
from pyperlib.coins import bitcoin


class CoinList(coins.CoinList):
    """A CoinList that contains many bitcoin-derived altcoins."""

    @staticmethod
    def make_coin(name, network, wif, ticker):
        """Create a new Coin type with the given attributes."""
        attr = {
            "name": name,
            "ticker": ticker,
            "wif_version": data.HexData(wif),
            "addr_version": data.HexData(network)
            }
        return type("Coin", (bitcoin.Coin,), attr)

    @classmethod
    def list(cls):
        """Make a list of Coin types from the data table below."""
        cl = []

        for args in coins:
            Coin = cls.make_coin(*args)
            cl.append(Coin)

        return cl


'''
The below code is derived from code that is copyright WalletGenerator.net.

The WalletGenerator.net software is available under The MIT License (MIT)
Copyright (c) 2014 WalletGenerator.net

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
'''

coins = [
    ("2GIVE",               "27", "a7", "2give"),
    ("42coin",              "08", "88", "42"),
    ("Acoin",               "17", "e6", "acoin"),
    ("Alphacoin",           "52", "d2", "apc"),
    ("Alqo",                "17", "c1", "alqo"),
    ("Animecoin",           "17", "97", "ani"),
    ("Anoncoin",            "17", "97", "anc"),
    ("Apexcoin",            "17", "97", "cpx"),
    ("Auroracoin",          "17", "97", "aur"),
    ("Aquariuscoin",        "17", "97", "arco"),
    ("BBQcoin",             "55", "d5", "bqc"),
    ("Biblepay",            "19", "b6", "bbp"),
    ("Bitcoin Cash",        "00", "80", "bch"),
    ("BitcoinDark",         "3c", "bc", "btcd"),
    ("BitcoinGold",         "26", "80", "btg"),
    ("Bitconnect",          "12", "92", "bcc"),
    ("Birdcoin",            "2f", "af", "brd"),
    ("BitSynq",             "3f", "bf", "synq"),
    ("BitZeny",             "51", "80", "zny"),
    ("Blackcoin",           "19", "99", "blk"),
    ("BlackJack",           "15", "95", "jack"),
    ("BlockNet",            "1a", "9a", "block"),
    ("BolivarCoin",         "55", "d5", "boli"),
    ("BoxyCoin",            "4b", "cb", "boxy"),
    ("BunnyCoin",           "1a", "9a", "bun"),
    ("Cagecoin",            "1f", "9f", "cage"),
    ("Canada eCoin",        "1c", "9c", "cdn"),
    ("CannabisCoin",        "1c", "9c", "cann"),
    ("Capricoin",           "1c", "9c", "cpc"),
    ("Cassubian Detk",      "1e", "9e", "cdt"),
    ("CashCoin",            "22", "a2", "cash"),
    ("Catcoin",             "15", "95", "cat"),
    ("ChainCoin",           "1c", "9c", "chc"),
    ("ColossusCoinXT",      "1e", "d4", "colx"),
    ("Condensate",          "3c", "bc", "rain"),
    ("Copico",              "1c", "90", "xcpo"),
    ("Corgicoin",           "1c", "9c", "corg"),
    ("CryptoBullion",       "0b", "8b", "cbx"),
    ("CryptoClub",          "23", "a3", "ccb"),
    ("Cryptoescudo",        "1c", "9c", "cesc"),
    ("Cryptonite",          "1c", "80", "xcn"),
    ("CryptoWisdomCoin",    "49", "87", "cwis"),
    ("C2coin",              "1c", "9c", "c2"),
    ("Dash",                "4c", "cc", "dash"),
    ("DeafDollars",         "30", "b0", "deaf"),
    ("DeepOnion",           "1f", "9f", "onion"),
    ("Deutsche eMark",      "35", "b5", "dem"),
    ("Devcoin",             "00", "80", "dvc"),
    ("DigiByte",            "1e", "9e", "dgb"),
    ("Digitalcoin",         "1e", "9e", "dgc"),
    ("DNotes",              "1f", "9f", "note"),
    ("Dogecoin",            "1e", "9e", "doge"),
    ("DogecoinDark",        "1e", "9e", "doged"),
    ("eGulden",             "30", "b0", "efl"),
    ("eKrona",              "2d", "ad", "krn"),
    ("ELECTRA",             "21", "a1", "eca"),
    ("Emerald",             "22", "a2", "emd"),
    ("Emercoin",            "21", "80", "emc"),
    ("EnergyCoin",          "5c", "dc", "enrg"),
    ("Espers",              "21", "a1", "esp"),
    ("Fastcoin",            "60", "e0", "fst"),
    ("Feathercoin",         "0e", "8e", "ftc"),
    ("Fedoracoin",          "21", "80", "tips"),
    ("Fibre",               "23", "a3", "fibre"),
    ("Florincoin",          "23", "b0", "flo"),
    ("Flurbo",              "23", "30", "flb"),
    ("Fluttercoin",         "23", "a3", "flt"),
    ("FrazCoin",            "23", "A3", "fraz"),
    ("Freicoin",            "00", "80", "frc"),
    ("FUDcoin",             "23", "a3", ""),
    ("Fuelcoin",            "24", "80", "fc2"),
    ("Fujicoin",            "24", "a4", "fjc"),
    ("Gaben Coin",          "10", "90", "gbn"),
    ("GlobalBoost",         "26", "a6", "bsty"),
    ("Goodcoin",            "26", "a6", "good"),
    ("GridcoinResearch",    "3e", "be", "grc"),
    ("Gulden",              "26", "a6", "nlg"),
    ("Guncoin",             "27", "a7", "gun"),
    ("HamRadioCoin",        "00", "80", "ham"),
    ("HOdlcoin",            "28", "a8", "hodl"),
    ("HTMLCoin",            "29", "a9", "html"),
    ("HyperStake",          "75", "f5", "hyp"),
    ("Imperium Coin",       "30", "b0", "mprm"),
    ("IncaKoin",            "35", "b5", "nka"),
    ("IncognitoCoin",       "00", "80", "icg"),
    ("Influxcoin",          "66", "e6", "infx"),
    ("Innox",               "4b", "cb", ""),
    ("IridiumCoin",         "30", "b0", "ird"),
    ("iCash",               "66", "cc", "icash"),
    ("iXcoin",              "8a", "80", "ixc"),
    ("Judgecoin",           "2b", "ab", "judge"),
    ("Jumbucks",            "2b", "ab", "jbs"),
    ("KHcoin",              "30", "b0", ""),
    ("Lanacoin",            "30", "b0", "lana"),
    ("Latium",              "17", "80", "lat"),
    ("Litecoin",            "30", "b0", "ltc"),
    ("LiteDoge",            "5a", "ab", "ldoge"),
    ("LoMoCoin",            "30", "b0", "lmc"),
    ("MadbyteCoin",         "32", "6e", "mbyt"),
    ("MagicInternetMoney",  "30", "b0", "mim"),
    ("Magicoin",            "14", "94", "mage"),
    ("Marscoin",            "32", "b2", "mars"),
    ("MarteXcoin",          "32", "b2", "mtx"),
    ("MasterDoge",          "33", "8b", "mdoge"),
    ("Mazacoin",            "32", "e0", "mzc"),
    ("Megacoin",            "32", "b2", "mec"),
    ("MintCoin",            "33", "b3", "mint"),
    ("MobiusCoin",          "00", "80", "mobi"),
    ("MonetaryUnit",        "10", "7e", "mue"),
    ("Monocle",             "32", "b2", "mon"),
    ("MoonCoin",            "03", "83", "moon"),
    ("Myriadcoin",          "32", "b2", "xmy"),
    ("NameCoin",            "34", "80", "nmc"),
    ("Navcoin",             "35", "96", "nav"),
    ("NeedleCoin",          "35", "b5", "ndc"),
    ("Neoscoin",            "35", "b1", "neos"),
    ("Nevacoin",            "35", "b1", "neva"),
    ("Novacoin",            "08", "88", "nvc"),
    ("Nubits",              "19", "bf", "usnbt"),
    ("Nyancoin",            "2d", "ad", "nyan"),
    ("Ocupy",               "73", "f3", "ocupy"),
    ("Omnicoin",            "73", "f3", "omc"),
    ("Onyxcoin",            "73", "f3", "onx"),
    ("Particl",             "38", "6c", "part"),
    ("Paycoin",             "37", "b7", "xpy"),
    ("Pandacoin",           "37", "b7", "pnd"),
    ("ParkByte",            "37", "b7", "pkb"),
    ("Pesetacoin",          "2f", "af", "ptc"),
    ("PHCoin",              "37", "b7", "phc"),
    ("PhoenixCoin",         "38", "b8", "pxc"),
    ("Pinkcoin",            "03", "83", "pink"),
    ("PIVX",                "1e", "d4", "pivx"),
    ("Peercoin",            "37", "b7", "ppc"),
    ("Potcoin",             "37", "b7", "pot"),
    ("Primecoin",           "17", "97", "xpm"),
    ("ProsperCoin Classic", "3a", "ba", "prc"),
    ("Quark",               "3a", "ba", "qrk"),
    ("Qubitcoin",           "26", "e0", "q2c"),
    ("Reddcoin",            "3d", "bd", "rdd"),
    ("Riecoin",             "3c", "80", "ric"),
    ("Rimbit",              "3c", "bc", "rbt"),
    ("ROIcoin",             "3c", "80", "roi"),
    ("Rubycoin",            "3c", "bc", "rby"),
    ("Rupaya",              "3c", "bc", "rupx"),
    ("Sambacoin",           "3e", "be", "smb"),
    ("SecKCoin",            "3f", "bf", ""),
    ("SibCoin",             "3f", "80", "sib"),
    ("SixEleven",           "34", "80", "611"),
    ("SmileyCoin",          "19", "99", "smly"),
    ("SongCoin",            "3f", "bf", "song"),
    ("SpreadCoin",          "3f", "bf", "spr"),
    ("StealthCoin",         "3e", "be", "xst"),
    ("Stratis",             "3f", "bf", "strat"),
    ("SwagBucks",           "3f", "99", "bucks"),
    ("Syscoin",             "00", "80", "sys"),
    ("Tajcoin",             "41", "6f", "taj"),
    ("Terracoin",           "00", "80", "trc"),
    ("Titcoin",             "00", "80", "tit"),
    ("TittieCoin",          "41", "c1", "ttc"),
    ("Topcoin",             "42", "c2", "top"),
    ("TransferCoin",        "42", "99", "tx"),
    ("TreasureHuntCoin",    "32", "b2", ""),
    ("TrezarCoin",          "42", "C2", "tzc"),
    ("Unobtanium",          "82", "e0", "uno"),
    ("USDe",                "26", "a6", "usde"),
    ("Vcash",               "47", "c7", "xvc"),
    ("Versioncoin",         "46", "c6", "v"),
    ("VergeCoin",           "1e", "9e", "xvg"),
    ("VertCoin",            "47", "80", "vtc"),
    ("Viacoin",             "47", "c7", "via"),
    ("VikingCoin",          "46", "56", "vik"),
    ("W2Coin",              "49", "c9", ""),
    ("WACoins",             "49", "c9", ""),
    ("WankCoin",            "00", "80", "wkc"),
    ("WeAreSatoshiCoin",    "87", "97", "wsx"),
    ("WorldCoin",           "49", "c9", "wdc"),
    ("Experience Points",   "4b", "cb", "xp"),
    ("Zetacoin",            "50", "E0", "zet"),
    ("Bitcoin Testnet",     "6f", "ef", "test")
]
