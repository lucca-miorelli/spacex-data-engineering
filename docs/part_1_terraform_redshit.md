# Terraform Redshift

Terraform is an open-source Infrastructure as Code (IaC) software tool that provides a consistent CLI workflow to manage hundreds of cloud services. It codifies APIs into declarative configuration files which can be shared amongst team members, treated as code, edited, reviewed, and versioned.

## Terraform Redshift open-source module

While it's possible to write our own Terraform configuration for creating a Redshift cluster on AWS, there are several reasons why using the ready-to-use [Redshift open-source module](https://github.com/terraform-aws-modules/terraform-aws-redshift/tree/master) is beneficial:

1. **Time-saving**: This module has already been written and tested. We don't need to spend time writing and testing our own configuration, which lets we focus on other aspects of our project.

2. **Best practices**: The module is developed by the community and follows the best practices for Terraform and AWS.

3. **Maintained**: The module is actively maintained. Any updates or necessary changes based on new versions of Terraform or AWS services are likely to be implemented in the module.

4. **Customizable**: While the module provides a set of sensible defaults, it can be easily customized to fit our specific needs.

To use the module, we'd include something like this in the Terraform configuration:

```hcl
module "redshift" {
  source = "terraform-aws-modules/redshift/aws"
  version = "~> 2.0"

  cluster_identifier      = "my-cluster"
  database_name           = "mydb"
  master_username         = "user"
  master_password         = "password"
  node_type               = "dc1.large"
  cluster_type            = "single-node"
  vpc_security_group_ids  = ["sg-12345678"]
}
```

## VPC and Network Considerations

Setting up a Redshift cluster requires careful consideration of networking configurations. Ideally, the cluster should be situated in a private subnet of a Virtual Private Cloud (VPC) for enhanced isolation and control. Private subnets

Configuration aspects like subnets, route tables, network access control lists (ACLs) - at a network level - , and security groups - at instance level - are critical for regulating traffic to the cluster, in both network and instance/cluster levels. For services in the AWS environment we can setup VCP endpoints. 

For better maintainability of advanced network requirements, I'd opt for using a Terraform module like the [VPC module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest), which creates a customizable VPC complete with public and private subnets, route tables, and network ACLs, etc.