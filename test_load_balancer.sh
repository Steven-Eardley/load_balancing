#!/usr/bin/env bash

count=0;
status=0;

while [[ ${count} -lt 100 ]]
    do
        ((count=count+1))
        resp=$(curl -s localhost:8080);
        respcount=${resp#Hello*count }

        echo ${resp}

        # We should exit if the counts are out of sync
        if [[ ${count} != ${respcount} ]]
        then
            echo "Local and remote sequence counts differ: local $count, remote $respcount";
            status=1;
            #break;
        fi
        #sleep .5s
    done

exit ${status};
