# **AWS Multi-Environment Cloud Architecture**

## **1. Updated High-Level Network Diagram**

The AWS **Multi-Environment Architecture** follows a **multi-account structure** under **AWS Organizations**, leveraging **[AWS Resource Access Manager (RAM)](https://aws.amazon.com/ram/)** to securely share resources across **Dev, Test, and Prod accounts**. 

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

#### **🔹 AWS RAM Resource Share**
```hcl
resource "aws_ram_resource_share" "share" {
  for_each                 = var.environments
  name                     = "ram-share-${each.key}"
  allow_external_principals = false
}
```

#### **🔹 AWS RAM Subnet Association**
```hcl
resource "aws_ram_resource_association" "subnet_association" {
  for_each = var.subnet_arns
  resource_share_arn = aws_ram_resource_share.share[each.key].arn
  resource_arn       = each.value
}
```

#### **🔹 AWS RAM Principal Association**
```hcl
resource "aws_ram_principal_association" "principal" {
  for_each = var.environments
  resource_share_arn = aws_ram_resource_share.share[each.key].arn
  principal = each.value  # AWS Account ID or Organization ARN
}
```

#### **🔹 Terraform Backend Configuration (S3 State)**
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

#### **🔹 Terraform Outputs**
```hcl
output "resource_share_arns" {
  value = { for k, share in aws_ram_resource_share.share : k => share.arn }
}
```

---

## **3. Key Recommendations**

### ✅ **Security & Compliance**
- **AWS RAM restricts access** to specific AWS **accounts or Org Units**.
- **IAM Roles + Least Privilege** prevent unauthorized cross-account access.
- **KMS encrypts all RDS, S3, and sensitive data**.
- **Centralized logging in S3** for compliance auditing.

### 🚀 **Scalability & High Availability**
- **Multi-AZ RDS** ensures automatic failover.
- **Auto Scaling Groups (ASG) & ECS** handle increasing traffic.
- **AWS RAM prevents redundant resources** across environments.

### 💰 **Cost Optimization**
- **Cross-account resource sharing via AWS RAM** reduces duplicated services.
- **Right-sized EC2 & Reserved Instances** optimize costs.
- **S3 Centralized Logging** minimizes per-account logging expenses.

---

## **4. Architecture and Design Answers**

1. **How would you improve the current architecture to support future growth?**
   - Implement **VPC Peering** or **AWS Transit Gateway** for better interconnectivity.
   - Adopt **serverless** architectures where applicable.
   - Use **EKS or ECS Fargate** for containerized workloads.

2. **How would you support multiple environments (dev, test, prod)?**
   - Maintain separate **AWS accounts per environment**.
   - Use **AWS RAM** for sharing necessary resources securely.

3. **How would you ensure high availability and fault tolerance?**
   - Enable **Multi-AZ deployments** for RDS and ALB.
   - Use **Auto Scaling Groups** for elasticity.
   - Implement **cross-region replication** for disaster recovery.

---

## **5. Automation and Terraform Answers**

1. **How would you automate deployments?**
   - Use **Terraform with modularized infrastructure**.
   - Implement **CI/CD pipelines with GitHub Actions or AWS CodePipeline**.

2. **How would you manage Terraform state securely?**
   - Store state in **S3 with encryption**, using **DynamoDB for state locking**.

---

## **6. Compliance and Security Answers**

1. **How would you secure sensitive data?**
   - Use **AWS KMS encryption** for data at rest.
   - Apply **IAM policies with least privilege**.

2. **How would you ensure compliance?**
   - Use **AWS Config, GuardDuty, and Security Hub**.
   - Maintain **audit logs with CloudTrail and centralized S3 logging**.

---

## **7. Cost and Observability Answers**

1. **How would you optimize costs?**
   - Use **Reserved Instances and Savings Plans** for predictable workloads.
   - Leverage **Spot Instances** for non-critical tasks.

2. **What tools would you use for monitoring?**
   - Use **CloudWatch, AWS X-Ray, and centralized logging in S3**.
   - Implement **custom dashboards in Grafana or Datadog**.

---

## **Final Thoughts**

This design ensures **secure, scalable, and cost-effective** AWS infrastructure using **Terraform + AWS RAM** for **cross-account VPC resource sharing**.