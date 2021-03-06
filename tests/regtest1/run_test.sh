#!/usr/bin/env bash

# do not exit if any command fails for the initialization
# it will be reset before tests
set +e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${script_dir}

# find akrr and akrrregtest
which_akrr=$(which akrr 2> /dev/null)

if [ ! -x "${which_akrr}" ] ; then
    echo "Can not find akrr executable, should be in PATH"
    exit 1
fi

which_akrrregtest=$(which akrrregtest 2> /dev/null)

if [ ! -x "${which_akrrregtest}" ] ; then
    which_akrrregtest=$(readlink -e ../bin/akrrregtest)
fi

if [ ! -x "${which_akrrregtest}" ] ; then
    echo "Can not find akrr executable, should be in PATH"
    exit 1
fi

highlight='-e "\e[32,1m[AKRR_Reg_Test:1]\e[0m"'

echo $highlight "akrr to use: ${which_akrr}"
echo $highlight "akrrregtest to use: ${which_akrrregtest}"
echo $highlight "current work directory: $(pwd)"
#exit if any command fails
set -e

echo $highlight "Testing AKRR setup"
${which_akrrregtest} -v setup

${which_akrr} daemon status

echo $highlight "Testing AKRR resource adding "
${which_akrrregtest} -v resource add -r localhost

${which_akrr} daemon status

#edit some files
AKRR_CONF_DIR=$(dirname $(dirname ${which_akrr}))/etc
RES_CONF=$AKRR_CONF_DIR/resources/localhost/resource.conf

echo $highlight "Testing AKRR resource deployment "
#${which_akrrregtest} -v resource deploy -r localhost -n 1
${which_akrr} -v resource deploy -r localhost -n 1

${which_akrr} daemon status

echo $highlight "Adding second resource without deployment"
${which_akrrregtest} -v resource add -r localhost2
