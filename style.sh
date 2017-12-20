#!/usr/bin/env bash

function doc
{
    while read f
    do
        last=
        while read line
        do
            if echo "$last" | grep -Eq '^ *(class|def) '
            then
                if ! echo "$line" | grep -Eq '^""".*\."""$'
                then
                    echo "IMPROPER DOCS: $f: $last"
                fi
            fi
            last="$line"
        done < "$f"
    done
}

find . -name '*.py' | doc
