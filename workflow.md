# Workflow document

## Installing the AWS command line interface (CLI)

The easiest way to get the CLI is to use the Python package manager, PIP.  That requires first installing Python (instructions [here](https://heardlibrary.github.io/digital-scholarship/script/python/install/)).  The installation instructions are [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html), although you really just have to enter

```
pip3 install awscli
```

in the console.  You can test whether it's working by entering 

```
aws help
```

in the console.  If you get an error message, then you may need to add the executable to your system PATH variable.  There are instructons for that linked to the [installation page](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html). 

# Archiving work in GitHub

The overall goal is to create the code in such a way that it could be entirely recreated through a build system even if the AWS site were completely deleted.  As a practical matter, that means that the code should be pushed to GitHub from the local machine at regular intervals.  

Development of new code or significant modification of code should be done using branches, followed by pull requests to merge the changes into the master branch.  The pull request doesn't need to wait until the branch is "finished".  Rather it should be made as soon as there is something that needs to be discussed by the team.  The pull request automatically creates an item in the "In Progress" section  project board.  If the pull request is relevant to the current milestone, it should be dragged manually into the "Current Milestone" section.  

**Question: do we want to specify that the title of the pull request be in the same "As...I want...so that..." form as the issues?  Or should it be descriptive of the revised state of the master when the pull is complete?**

If it's helpful for a particular team member to review the pull request, a review request can be made at the point at which the pull request might be ready for the merge.

# Creating code

## Creating IAM roles and policies

AWS policies describe what an agent is allowed to do.  Roles group the policies so that the role can be assigned to a particular agent (e.g. application).  

In many cases, it is not necessary to create a policy, since there are many AWS managed policies that are built-in.  To see those policies on the AWS web interface, go to the IAM service, then click on the Policies link at the left.  The AWS managed policy names generally begin with "Amazon..." or "AWS..." and can be found by typing the kind of resource to be allowed (e.g. "lambda" in the search box.)

Policies can be created online by clicking on the "Create policy" button on the IAM service search page.  However, if we create our own policies, it would be better to use the CLI to do it so that it could be part of an automated build process.  The instructions for doing it are [here](https://docs.aws.amazon.com/cli/latest/reference/iam/create-policy.html).  The policy JSON should be stored in the iam/policies/ directory along with a corresponding bash script with a line an be run to create the policy.  

The situation with roles is similar in that they can be created online or by CLI.  First, the role should be created using the directions on [this page](https://docs.aws.amazon.com/cli/latest/reference/iam/create-role.html).  It is probably best not to attach the policy directly to the role.  Rather, after creating the role, attach an existing policy to it using [these instructions](https://docs.aws.amazon.com/cli/latest/reference/iam/attach-role-policy.html).

## IAM role records

Roles that have been created that might be reused should be recorded in [the iamRoldes.md](https://github.com/HeardLibrary/cloud-tvnews/blob/master/iamRoles.md) document.

## Creating Lambdas

For testing and debugging, it's convenient to create lambdas using the online editor.  However, for the purpose of archiving the function and making it possibe to rebuild the application, the lambda should be stored locally and pushed to GitHub.  

The actual Python scripts should be saved in the `lambdas` directory.  The script can't be uploaded until it's compressed into a ZIP file.  The .zip files should be stored in the `zips` subdirectory of `lambdas`.  The zip file must also include any modules that aren't included in the standard library, or by default by AWS.  Those files (which won't change in the way that the script itself will change) can be stored in an appropriately named subdirectory of the `zips` directory so that they can be inserted into any .zip file that needs to include them.  The lambda can be created using the CLI - see [this page](https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html) for details.  There is also an [update function code](https://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-code.html) command that can be used to replace the function.  The code still must be included in a .zip file.

A bash script that can be invoked to create the lambda should be saved in the `lambdas` folder.

## Creating step functions

Step functions can be created online or using the CLI as with the other items above.  Here's [the web page](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/create-state-machine.html) for creating a state machine using the CLI.  Updating the state machine is described [here](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/update-state-machine.html).  

The state machine JSON and a corresponding bash script for creating the step function should be stored in the `stateMachines` directory. 

A screenshot of the state machine diagram should be captured and inserted into the README.md page for the stateMachines directory.

----
Revised 2019-04-22
