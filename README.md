# aws-tags-convention-scanner
Can be used to scan AWS resources to check whether their tags match some convention defined in config.

## Config explained

 - `region` - aws region you want to retrieve resources from
 - `scan` - list of aws_resources you want to scan
    - `resource` - can be one of predefined aws_resources
    - `grouping_tag` - this is the most important tag, you expect that for tags matched by this tag will have the same values (by convention)
    - `tags` - tags you want to compare to each other to validate whether your convention is maintained

