#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate thumbor
source "$(pyenv prefix thumbor)/bin/activate"

while getopts :f:c: flag
do
    case "${flag}" in
        f) filepath=${OPTARG};;
        c) config_file=${OPTARG};;
    esac
done

if [ -z "$filepath" ]
then
      echo "-f <path> is required to run this script!"
      exit 1
fi
if [ -z "$config_file" ]
then
      echo "-c <path> is required to run this script!"
      exit 1
fi


mypy --config-file $config_file $filepath
