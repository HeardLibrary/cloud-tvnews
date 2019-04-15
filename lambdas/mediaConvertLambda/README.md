# Media Convert Lamda

This lambda starts (via events configured on s3 buckets) when a new metadata.xml file drops in any network bucket. The lambda opens the xml file and finds the "Actual Start Time." After converting this time to a few different formats, it updates the Media Convert settings file (json) to start a new Media Convert job.


----
Revised 2019-04-15
