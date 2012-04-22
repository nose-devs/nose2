#!/bin/bash


command -v nose2 >/dev/null >&2 || {
    source /usr/local/bin/virtualenvwrapper.sh
    workon nose2
}

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
                -w) nargs="$nargs -t"
                    skip="copy"
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
        copy)
            skip="no"
            nargs="$nargs $var"
            ;;
    esac
done

cd $root
nose2 $nargs
