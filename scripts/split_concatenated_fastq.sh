#!/bin/sh
# split fastq file in two file for cases where paired-end are concatened (not interlaced)
(gzip -dc  intput.fastq.gz) | awk -F"=" 'BEGIN {OFS = "\n"} {name = $0; getline seq; getline name2; getline phred; print name, substr(seq,0,int(length(seq)/2)), name2, substr(phred,0,int(length(seq)/2)) >> "intput-1.fastq"; print name, substr(seq,int(length(seq)/2)+1,length(seq)), name2, substr(phred,int(length(seq)/2)+1,length(seq)) >> "intput-2.fastq"}'
