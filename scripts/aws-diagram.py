"""
High-Level AWS Architecture Diagram with Multi-Account Setup
Using mingrammer's diagrams library: https://diagrams.mingrammer.com/
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.general import User
from diagrams.aws.management import OrganizationsAccount
from diagrams.aws.network import VPC, PublicSubnet, PrivateSubnet, NATGateway, InternetGateway
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB
from diagrams.aws.security import KMS
from diagrams.aws.storage import S3

with Diagram("AWS Multi-Env Architecture", show=False, direction="LR"):
    print(f"Diagram will be saved as: ./aws_multi_env_architecture.png")

    # Represent developer or end-user
    developer = User("Developer")

    # Shared Services / Security Account
    shared_services_acc = OrganizationsAccount("Shared Services/Security Acc")

    with Cluster("AWS Organization"):
        dev_account = OrganizationsAccount("Dev Account")
        test_account = OrganizationsAccount("Test Account")
        prod_account = OrganizationsAccount("Prod Account")

    # Example of a VPC in each account
    with Cluster("Dev VPC"):
        dev_igw = InternetGateway("IGW")
        dev_nat = NATGateway("NAT Gateway")

        with Cluster("Public Subnet"):
            dev_alb = ALB("Dev ALB")

        with Cluster("Private Subnet"):
            dev_ec2 = EC2("App Server")
            dev_db = RDS("Dev RDS")

    with Cluster("Test VPC"):
        test_igw = InternetGateway("IGW")
        test_nat = NATGateway("NAT Gateway")

        with Cluster("Public Subnet"):
            test_alb = ALB("Test ALB")

        with Cluster("Private Subnet"):
            test_ec2 = EC2("App Server")
            test_db = RDS("Test RDS")

    with Cluster("Prod VPC"):
        prod_igw = InternetGateway("IGW")
        prod_nat = NATGateway("NAT Gateway")

        with Cluster("Public Subnet"):
            prod_alb = ALB("Prod ALB")

        with Cluster("Private Subnet"):
            prod_ec2 = EC2("App Server")
            prod_db = RDS("Prod RDS")

    # KMS in each account for encryption
    kms_key = KMS("KMS Keys")

    # Shared S3 bucket for logs
    central_logs = S3("Central Log Bucket")

    # Connectivity / flows
    developer >> Edge(label="Deploy via CI/CD") >> dev_account
    developer >> Edge(label="Deploy via CI/CD") >> test_account
    developer >> Edge(label="Deploy via CI/CD") >> prod_account

    # VPC flows
    dev_alb >> dev_ec2 >> dev_db
    test_alb >> test_ec2 >> test_db
    prod_alb >> prod_ec2 >> prod_db

    # Central logs for all accounts
    dev_db >> central_logs
    test_db >> central_logs
    prod_db >> central_logs

    # Indicate that all RDS / S3 are encrypted with KMS
    kms_key - dev_db
    kms_key - test_db
    kms_key - prod_db
    kms_key - central_logs
