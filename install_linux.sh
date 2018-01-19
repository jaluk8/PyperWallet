#!/usr/bin/env bash

if [ ! -f install_linux.sh ]
then
    echo "Error: You must be in the PyperWallet folder to install."
    exit 1
fi

if [[ $(id -u) != 0 ]]
then
    echo "Error: You must be root to install."
    exit 1
fi

if [[ $1 == "--uninstall" ]]
then
    rm -rf /usr/local/src/PyperWallet
    rm /usr/local/bin/cpyper
    rm /usr/local/bin/gpyper
elif [[ $1 == "--install" ]]
then
mkdir -p /usr/local/src/PyperWallet
rm -rf /usr/local/src/PyperWallet/*  # Delete previous installs
cp -r * /usr/local/src/PyperWallet/
ln -s /usr/local/src/PyperWallet/cpyper.py /usr/local/bin/cpyper
ln -s /usr/local/src/PyperWallet/gpyper.py /usr/local/bin/gpyper
echo "Installed. Run cpyper or gpyper to try it out."
else
    echo "Invalid argument: $1"
    exit 1
fi
