## Executive Summary
The AWS **Multi-Environment Architecture** follows a **multi-account structure** under **AWS Organizations**, leveraging **[AWS Resource Access Manager (RAM)](https://aws.amazon.com/ram/)** to securely share resources across e.g **Dev and Prod accounts**. resource sharing. Key features include:
- Centralized security and compliance management
- Cost-effective resource sharing
- Automated deployment using Terraform
- Comprehensive monitoring and observability

# **AWS Multi-Environment Cloud Architecture**
## Architecture Decisions
1. **AWS RAM**: Chosen for secure resource sharing to reduce costs and complexity
2. **Multi-Account Strategy**: Provides strong isolation between environments
3. **Centralized NAT Gateway**: Reduces costs while maintaining security

## **1. Updated High-Level Network Diagram**

### **Key Components:**
- **AWS Organizations**: Enforces **multi-account isolation** for **Dev, Test, and Prod** environments.
- **VPC Per Account**: Each environment has its **own VPC**, ensuring strong isolation.
- **Subnets**:
  - **Public Subnets**: Contain **ALBs and NAT Gateways** for internet-facing components.
  - **Private Subnets**: Host **EC2 instances and RDS databases** for application workloads.
- **AWS RAM**:  
  - Shares **VPC resources (subnets, security groups)** across accounts securely.
  - Uses **cross-account IAM role permissions**.
- **Application Load Balancer (ALB)**: Routes **HTTP/HTTPS** traffic.
- **Auto Scaling Groups (ASG): Dynamically scales application workloads.
- **RDS with Multi-AZ**: Ensures **high availability**.
- **AWS KMS**: Encrypts **RDS, S3, and sensitive data**.
- **Centralized Logging (S3)**: All accounts store **logs in a shared S3 bucket**.

The architecture diagram (generated using Python **mingrammer's [`diagrams` library](https://diagrams.mingrammer.com/docs/nodes/aws)**) visually represents these components.

![AWS Shared VPC Architecture - Multi-Environment Design](scripts/aws_shared_vpc_architecture-3.png "AWS Multi-Environment Architecture Diagram")
---

## **2. Automation Example (Terraform Code)**

The Terraform implementation **automates AWS RAM-based resource sharing** across Dev, Test, and Prod environments.
> 📌 **Note**: The Terraform code and scripts for this implementation is available in my personal [GitHub repository](https://github.com/ayobuba/sand-curly-funicular).


### **Key Features:**
✅ **AWS RAM Resource Sharing** for **cross-account resource access**.  
✅ **Remote Terraform State Management** with **S3 + DynamoDB locking**.  
✅ **IAM-controlled resource sharing**, ensuring **least-privilege access**.

---

### **Terraform Code Snippets:**

#### **AWS RAM Resource Share**
```hcl
resource "aws_ram_resource_share" "share" {
  for_each                 = var.environments
  name                     = "ram-share-${each.key}"
  allow_external_principals = false
}
```

#### **2. AWS RAM Subnet Association**
```hcl
resource "aws_ram_resource_association" "subnet_association" {
  for_each = var.subnet_arns
  resource_share_arn = aws_ram_resource_share.share[each.key].arn
  resource_arn       = each.value
}
```

#### **AWS RAM Principal Association**
```hcl
resource "aws_ram_principal_association" "principal" {
  for_each = var.environments
  resource_share_arn = aws_ram_resource_share.share[each.key].arn
  principal = each.value  # AWS Account ID or Organization ARN
}
```

#### **Terraform Backend Configuration (S3 State)**
```hcl
terraform {
  backend "s3" {
    bucket         = "sandtech-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    use_lockfile   = true #S3 Backend Now Supports Native Locking
  }
}
```

#### **Terraform Module Use (VPC and RAM)**
```hcl
module "shared-vpc" {
  source       = "../../modules/vpc"
  vpc_cidr     = var.vpc_cidr
  vpc_name     = "shared-vpc"
  az           = var.az

  # We define subnets for dev, test, and prod
  subnets = {
    dev     = var.dev_subnet_cidr
    test    = var.staging_subnet_cidr
    prod    = var.prod_subnet_cidr
  }
}

module "resource-access-manager" {
  source        = "../../modules/ram"
  environments  = var.environments  # map of environment->account_arn
  subnet_arns   = module.shared-vpc.subnet_arns
}
```

#### **Terraform Outputs**
```hcl
output "resource_share_arns" {
  value = { for k, share in aws_ram_resource_share.share : k => share.arn }
}
```

#### **AWS Config Rule for ISO 27001 Compliance**
```hcl
resource "aws_config_config_rule" "iso27001_rds_encryption" {
  name        = "rds-storage-encryption"
  description = "Ensure RDS is encrypted to comply with ISO 27001"
  source {
    owner             = "AWS"
    source_identifier = "RDS_STORAGE_ENCRYPTED"
  }
}

### ISO 27001 Controls Implementation
   resource "aws_config_config_rule" "iam_password_policy" {
     name = "iam-password-policy"
     source {
       owner             = "AWS"
       source_identifier = "IAM_PASSWORD_POLICY"
     }
     input_parameters = jsonencode({
       RequireUppercaseCharacters = "true"
       RequireLowercaseCharacters = "true"
       RequireSymbols             = "true"
       RequireNumbers            = "true"
       MinimumPasswordLength     = "14"
       PasswordReusePrevention   = "24"
       MaxPasswordAge            = "90"
     })
   }
```
---

## **3. Key Recommendations**

### ✅ **Security & Compliance**
- **AWS RAM restricts access** to specific AWS **accounts or Org Units**.
- **IAM Roles + Least Privilege** prevent unauthorized cross-account access.
- **KMS encrypts all RDS, S3, and sensitive data**.
- **Centralized logging in S3** for compliance auditing.


###  **Scalability & High Availability**
- **Multi-AZ RDS** ensures automatic failover.
- **Auto Scaling Groups (ASG) & ECS** handle increasing traffic.
- **AWS RAM prevents redundant resources** across environments.

### 💵 **Cost Optimization**
- **Cross-account resource sharing via AWS RAM** reduces duplicated services.
- **Right-sized EC2 & Reserved Instances** optimize costs.
- **S3 Centralized Logging** minimizes per-account logging expenses.

---

## **I. Architecture and Design Answers**

1. **How would you improve the current architecture to support future growth and increased workloads?**
   - Implement **VPC Peering** or **AWS Transit Gateway** for better interconnectivity.
   - Adopt **serverless** architectures where applicable.
   - Use **EKS or ECS Fargate** for containerized workloads.

2. **What approach would you take to support multiple environments (dev, test, prod)?**
   - Maintain separate **AWS accounts per environment**.
   - Use **AWS RAM** for sharing necessary resources securely.

3. **How would you ensure high availability and fault tolerance?**
   - Enable **Multi-AZ deployments** for RDS and ALB.
   - Use **Auto Scaling Groups** for elasticity.
   - Implement **cross-region replication** for disaster recovery.

---

## **II. Automation and Terraform Answers**

1. **How would you approach automating the deployment of this environment?**
   - Use **Terraform with modularized infrastructure**.
   - Implement **CI/CD pipelines with GitHub Actions or AWS CodePipeline**.

2. **What would be your strategy for securely managing Terraform state in a multi-environment or multi-account setup?**
   - S3 Backend Configuration with Native Locking for statefiles (DynamoDB not needed when it is released to a major version)
   - MFA delete protection
   - CloudWatch alerts for state modifications


---

## **III. Compliance and Security Answers**

1. **How would you secure sensitive client data in this environment??**
   - Use **AWS KMS encryption** for data at rest.
   - Apply **IAM policies with least privilege**.

2. **How would your design ensure compliance with industry standard i.e ISO 27001, GDPR, or similar standards.?**
   - Use **AWS Config** to enforce compliance rules.
   - Maintain **audit logs with CloudTrail and centralized S3 logging**.



## **7. Cost and Observability Answers**

1. **How would you optimize costs?**
   - Use **Reserved Instances and Savings Plans** for predictable workloads.
   - Leverage **Spot Instances** for non-critical tasks.
   - **[cloud-nuke](https://github.com/gruntwork-io/cloud-nuke)**: A tool for cleaning up AWS resources. Useful for:
     - Removing non-critical workloads or managed services if forgotten
     - Cleaning up development and testing environments
     - Cost optimization by ensuring unused resources are removed
   - setup **budgets and alerts** to monitor costs.

2. **What tools would you use for monitoring?**
   - Use **CloudWatch** for API activity and centralized logging.
   - Use **AWS X-Ray** for tracing and debugging
   - **AWS CloudTrail** for auditing and compliance of all API's.


---

## **Final Thoughts**

This design ensures **secure, scalable, and cost-effective** AWS infrastructure using **Terraform + AWS RAM** for **cross-account VPC resource sharing**.