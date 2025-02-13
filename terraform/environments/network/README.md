<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_resource-access-manager"></a> [resource-access-manager](#module\_resource-access-manager) | ../../modules/ram | n/a |
| <a name="module_shared-vpc"></a> [shared-vpc](#module\_shared-vpc) | ../../modules/vpc | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_az"></a> [az](#input\_az) | n/a | `string` | `"us-east-1a"` | no |
| <a name="input_dev_subnet_cidr"></a> [dev\_subnet\_cidr](#input\_dev\_subnet\_cidr) | n/a | `string` | `"10.10.1.0/24"` | no |
| <a name="input_environments"></a> [environments](#input\_environments) | n/a | `map(string)` | `{}` | no |
| <a name="input_prod_subnet_cidr"></a> [prod\_subnet\_cidr](#input\_prod\_subnet\_cidr) | n/a | `string` | `"10.10.3.0/24"` | no |
| <a name="input_staging_subnet_cidr"></a> [staging\_subnet\_cidr](#input\_staging\_subnet\_cidr) | n/a | `string` | `"10.10.2.0/24"` | no |
| <a name="input_vpc_cidr"></a> [vpc\_cidr](#input\_vpc\_cidr) | n/a | `string` | `"10.10.0.0/16"` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->