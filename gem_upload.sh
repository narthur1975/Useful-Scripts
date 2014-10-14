#!/bin/bash

GEMS=$(</home/narthur/gemlist.txt)

for GEM in $GEMS
do
gem="$GEM.gem"
cd /home/narthur/gems_for_upload/
echo gem nexus $gem
gem nexus $gem 2>&1 | tee -a /home/narthur/output2.log
#echo gem nexus $gem 2>&1 | tee output.log
done

