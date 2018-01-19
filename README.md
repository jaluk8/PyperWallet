# PyperWallet

## Description
PyperWallet is an advanced and extendable paper wallet generator written in Python for various types of cryptocurrencies. It currently supports Bitcoin, Ethereum, Litecoin, and 180 more cryptocurrencies. The full list can be found at the bottom of this page. Only a command-line interface is available right now, so check back later if you would rather use a GUI.

## Features
* Generating addresses
* Importing private keys and addresses
* Verifying private keys and addresses
* Importing using a "brain wallet" phrase (sha256)
* Encrypting private keys with bip38
* Displaying wallet information in text form

## Upcoming features
* More coins
* Making paper wallets (This one is kind of important)
* A GUI

## Installation guide
In order to install PyperWallet, you will first need to install Python 3.6. This varies depending on your operating system.

Next, you need to install the required dependencies. This pip command should install them all.
```
pip3 install cryptography pysha3 PyQt5
```
Then download this repository and put wherever you want on your computer. The `cpyper.py` file will start the command line interface. If you want to properly install the program as a system command (linux only), run `install_linux.sh --install` as root.

## Why PyperWallet?
PyperWallet was made using three major design decisions:
1. Use Python to get clean, readable code
2. Include a large amount of testing and documentation
3. Use modular design to allow for extensibility

Python code is generally rather easy to read. Since most cryptographic functions are handled by a trusted library, the code is also fairly short. This makes it easy for other developers to read through the code and check for vulnerabilities. This is vital for a wallet generator.

Another aspect of PyperWallet is the large amount of publicly-viewable tests and comments. As a rule of thumb, for every line of regular code added to the project there is a line of testing code. Every class and function is also documented by at least one comment explaining its function. The intent is to make all aspects of this project's security clearly visible.

Due to its modular design, PyperWallet can also be extended easily. Supporting more cryptocurrencies, wallet formats, and encryption schemes requires minimal work. For example, it took less than 100 lines of code to add Ethereum support to what is otherwise a Bitcoin wallet generator.

Naturally, the design choices behind PyperWallet have some issues. It will never be quite as easy to use or install as other wallet generators. It is also not something you can use on mobile devices (without significant effort). With that said, I believe PyperWallet's features will make it a useful tool for advanced paper wallet users.

## Development guide
If you want to develop some code for PyperWallet, just download these dependencies. Then you can use run_test.sh to run the unit tests and style.sh to run the style checker.
* python3-pycodestyle
* python3-autopep8
