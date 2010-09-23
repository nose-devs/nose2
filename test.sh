#!/bin/bash

. ~/.local/bin/virtualenvwrapper.sh
workon unit2

nargs=""
skip="no"
root=`dirname $0`

for var in "$@"
do
    case "$skip" in
        no)
            case "$var" in
                -v)  nargs="$nargs -v"
                    ;;
                --pdb) nargs="$nargs --debug"
                    ;;
                -w) skip="yes"
                    ;;
                -c) skip="yes"
                    ;;
                # filename to mod name, : to .
                *)
                    l="${#root}"+1
                    var="${var:$l}"
                    var="${var//\//.}"
                    var="${var//.py/}"
                    nargs="$nargs ${var//:/.}"
                    ;;
            esac
            ;;
        yes)
            skip="no"
            ;;
    esac
done

cd $root
nose2 $nargs
