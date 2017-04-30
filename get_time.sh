#!/bin/bash
ps aux|grep "python3.*SansanoBot"|sed -e "s/:/ /g"|head -n 1|awk '{print "Sansano bot total runtime: " int($10/24) " days and " $10%24+$11 " hours" }'
