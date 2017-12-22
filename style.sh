#!/usr/bin/env bash

function doc
{
    last=
    while read line
    do
        if echo "$last" | grep -Eq '^ *(class|def) '
        then
            if ! echo "$line" | grep -Eq '^""".*\."""$'
            then
                echo "IMPROPER DOCS: $1: $last"
            fi
        fi
        last="$line"
    done < "$1"
}

function pep8
{
    pycodestyle $1
}

function fix
{
    autopep8 --in-place $1
}

function run_check
{
    while read f
    do
        for t in $@
        do
            $t $f
        done
    done < <(find . -name '*.py')
}

case "$1"
in
    "")
        run_check pep8 doc
        ;;
    fix)
        run_check fix
        ./run_tests.sh
        ;;
    *)
        echo "Invalid parameter: $1"
        exit 1
        ;;
esac
