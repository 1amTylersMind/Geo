#!/bin/bash
for i in {1..254..1};do host $i'.'$i'.'$i'.'$i;sleep .2; done
#EOF
