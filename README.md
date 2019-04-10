# Cloud TV News
The goal of this project is to build a data pipeline for the Vanderbilt Television News Archive to replace the existing perl-based system. The data pipeline runs on [Amazon Web Services](https://aws.amazon.com/) using the [AWS Step Functions](https://aws.amazon.com/step-functions/). The code is primarily written in Python and configuration files are primarily JSON.

## Documentation

The documentation for Cloud TV News is maintained on a [Github Wiki](https://github.com/HeardLibrary/cloud-tvnews/wiki).


## Repo structure

```
├── README.md                  : Description of this repository
├── iamRoles.md                : list of potentially reusable IAM permissions roles
├── LICENSE                    : GNU General Public License v3.0 for repo
│
├── lambdas                    : scripts for current projects
│   ├──                        : 
│   │
│   └── zips                   : directory for zipped lambda packages ready for CLI upload
│ 
├── stateMachines              : Amazon State Language (ASL) code describing state machines
    └── serverlessApp.json     : state machine for overall workflow
```

----
Revised 2019-04-10
