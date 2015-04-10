#!/usr/bin/env bash


# http://goo.gl/9jGOA
removedup() {
    if [[ $# == 0 ]]; then
        return
    fi 
    filename=$1
    cp ${filename} ${filename}.org
    awk '!x[$0]++' ${filename}.org > ${filename}
    echo "-- done"
}
