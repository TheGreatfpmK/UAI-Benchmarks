#!/bin/bash

storm=""
paynt=""
prism=""
additional=false
#logs="logs"


function storm_log_dirs() {  
    mkdir -p "logs/storm-logs/best"
    mkdir -p "logs/storm-logs/first"
    mkdir -p "logs/storm-logs/over-approximation"
}

function paynt_log_dirs() {
    mkdir -p "logs/paynt-logs/best"
    mkdir -p "logs/paynt-logs/fastest"
}

function paynt_additional_dir() {
    mkdir -p "logs/additional-logs"
}

function prism_log_dirs() {
    mkdir -p "logs/prism-logs"
}

while getopts s:p:i:x flag
do
    case "${flag}" in
        s) storm=${OPTARG};;
        p) paynt=${OPTARG};;
        i) prism=${OPTARG};;
        x) additional=true;;
    esac
done


if [ "${storm}" != "" ]
then
    storm_log_dirs

    python3 storm-benchmark.py "${storm}"
fi

if [ "${paynt}" != "" ]
then
    paynt_log_dirs

    python3 paynt-benchmark.py "${paynt}"

    if [ "${additional}" = true ]
    then
        paynt_additional_dir
        
        python3 additional.py
    fi
fi

if [ "${prism}" != "" ]
then
    prism_log_dirs

    python3 prism-benchmark.py "${prism}"
fi


mkdir -p "lol"