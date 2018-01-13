#!/usr/bin/env bash

function doc
{
    status=
    last=
    while read line
    do
        if [[ -z $status ]]
        then
            if echo "$line" | grep -Eq '^ *(class|def) '
            then
                status=start
                last="$line"
            fi
        fi

        if [[ $status == start ]]
        then
            if echo "$line" | grep -Eq ':$'
            then
                status=end
                continue
            fi
        fi

        if [[ $status == end ]]
        then
            if echo "$line" | grep -Eq '^""".*\."""$'
            then
                status=
            else
                echo "IMPROPER DOCS: $1: $last"
                status=
            fi
        fi
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
