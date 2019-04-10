# Lambdas

Code repository for lambdas

The lambda name is the label for AWS.  The handler is the concatenation of the filename (minus `.py`), a dot, and the name of the function that fires when the lambda is invoked (usually `lambda_handler`).  The state label is the label used in the ASL code for the state that invokes the lambda.  The notes should include any changes affecting interoperability of the function when the version is incremented.

When code is ready for deployment, it should be packaged into a `.zip` file in the `zips` subdirectory of this one.

| ARN | version label | lambda name | handler | state label | notes |
|---|---|---|---|---|---|---|
| | | | | | | |

----
Revised 2019-04-10
