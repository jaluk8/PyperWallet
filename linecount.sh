#!/usr/bin/env bash

git diff --dirstat Initial HEAD pyperlib tests
git diff --shortstat Initial HEAD tests/*.py pyperlib/*.py *.py pyperlib/*/*.py
