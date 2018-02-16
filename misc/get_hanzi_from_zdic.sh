#!/usr/bin/env bash

function get_hanzi()
{
    curl "https://www.zdic.net/hans/$1" -s > "./out/$1.txt"
    sleep 1
}

mkdir ./out

export -f get_hanzi
cat "$1" | parallel -j 1 get_hanzi "{}"
