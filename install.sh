#!/bin/bash

install () {
    for file in $(ls | grep -E '.*\.sh$' | grep -Fvx 'install.sh'); do
        source "${file}"
    done;

    echo '. ${HOME}/.pdxjohnnyrc' | tee -a ~/.bashrc ~/.bash_profile
}

install
