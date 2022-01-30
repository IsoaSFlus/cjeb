#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd "$BASEDIR"

cat header.txt > hanma.txt
cat ../misc/mb.txt >> hanma.txt

mkdir build
cd build
cmake ../
make
