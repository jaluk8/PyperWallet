# PyperWallet

## Description
*NOTE: This project is no longer maintained and should not be used.*

PyperWallet is an extendable wallet generator written in Python for various types of cryptocurrencies. It currently supports Bitcoin, Ethereum, Litecoin, and 180 more cryptocurrencies. The full list can be found at the bottom of this page. A GUI is available, but the CLI client is recommended as it is more advanced.

## Features
* Generating addresses
* Importing private keys and addresses
* Verifying private keys and addresses
* Importing using a "brain wallet" phrase (sha256)
* Encrypting private keys with bip38
* Displaying wallet information in text form

## Installation guide
In order to install PyperWallet, you will first need to install Python 3.6. This varies depending on your operating system.

Next, you need to install the required dependencies. This pip command should install them all.
```
pip3 install cryptography pysha3 PyQt5
```
Then download this repository and put wherever you want on your computer. The `cpyper.py` file will start the command line interface. If you want to properly install the program as a system command (linux only), run `install_linux.sh --install` as root.

## Development guide
If you want to develop some code for PyperWallet, just download these dependencies. Then you can use run_test.sh to run the unit tests and style.sh to run the style checker.
* python3-pycodestyle
* python3-autopep8
