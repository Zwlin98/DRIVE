# DRIVE

Dataset and source code of DRIVE paper. 

In this paper, we propose a novel approach DRIVE (**D**ockerfiles **R**ule m**I**ning and **V**iolation d**E**tection) to identify general patterns in Dockerfiles with moderate human participation. 

DRIVE is able to identify new rules which have not been discovered by previous approaches.  Moreover, given the identified rules, DRIVE can detect violations of such patterns by analysing input Dockerfiles.

## Approach

Organized according to the structure of the approach part of the paper. 

+ 00-datasets: including the initial dataset.
+ 01-parse: source code for parsing and subsution.
+ 03-group-by-command: source code command-based grouping.
+ 04-filter-and-encode: source code for preparing data mining.
+ 05-rule-mining: source code for the rule mining and rule summarization.


## Evaluate

+ datasets: D1,D2,D3 dataset are provided.
+ rq1: source code for RQ1(How effective is the rule mining component of DRIVE?)
+ rq2: source code for RQ2(How effective is the rule summarization component of DRIVE?)
+ rq3: source code for RQ3(How effective is the rule mining component of DRIVE?)
