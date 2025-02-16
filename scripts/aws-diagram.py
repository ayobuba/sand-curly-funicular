from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, ALB, NATGateway, PrivateSubnet, PublicSubnet
from diagrams.aws.compute import EC2AutoScaling, EC2
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch, Organizations, Cloudformation, Config
from diagrams.aws.security import IAM, WAF, KMS
from diagrams.aws.storage import S3

# Define output file path
diagram_path = "aws_shared_vpc_architecture-3"

with Diagram(
        "AWS Shared VPC Architecture (With Compliance)",
        show=False,
        filename=diagram_path,
        outformat="png",
        direction="TB"
):
    # Shared VPC (AWS Account 1)
    with Cluster("Shared VPC (AWS Account 1)"):
        shared_vpc = VPC("Shared VPC")
        waf = WAF("WAF")
        alb = ALB("ALB")
        rds = RDS("RDS (Private IP Accessible)")
        ram = Cloudformation("AWS RAM (Resource Access Manager)")

        # NAT Gateway inside Public Subnet
        with Cluster("Public Subnet"):
            public_subnet = PublicSubnet("Public Subnet")
            nat = NATGateway("NAT Gateway")

        # Security and Monitoring
        cloudwatch = Cloudwatch("CloudWatch")
        cloudtrail = Cloudwatch("CloudTrail")  # Captures AWS API logs
        aws_config = Config("AWS Config (ISO 27001)")  # AWS Config for Compliance
        iam = IAM("IAM")
        kms = KMS("KMS")

        # Centralized Logging
        with Cluster("Centralized Logging"):
            logs = Cloudwatch("CloudWatch Logs")
            log_bucket = S3("Audit Archive")
            logs >> log_bucket
            cloudtrail >> log_bucket  # CloudTrail logs stored in S3

        # AWS Config & CloudTrail Monitor Resources for Compliance
        aws_config >> Edge(label="Monitors Compliance") >> [alb, rds, iam, ram]  # Compliance tracking
        cloudtrail >> Edge(label="API Logs") >> logs  # CloudTrail logs to CloudWatch Logs

        # CloudWatch only monitors logs
        cloudwatch >> logs

        # IAM only controls RAM and logs
        iam >> ram
        iam >> Edge(label="Access Control") >> logs

        # ALB, NAT, and RDS Send Logs to CloudWatch
        alb >> logs
        nat >> logs
        rds >> logs

    #  LEFT SIDE: Dev (Account 2)
    with Cluster("Dev (Account 2)"):
        dev_org = Organizations("Dev Org")
        dev_private_subnet = PrivateSubnet("Dev Private Subnet")
        dev_autoscaling = EC2AutoScaling("Dev ASG")
        client_a_dev = EC2("Client A Dev")
        client_b_dev = EC2("Client B Dev")

        dev_org >> dev_private_subnet >> dev_autoscaling >> [client_a_dev, client_b_dev]
        [client_a_dev, client_b_dev] >> logs

    #  RIGHT SIDE: Prod (Account 3)
    with Cluster("Prod (Account 3)"):
        prod_org = Organizations("Prod Org")
        prod_private_subnet = PrivateSubnet("Prod Private Subnet")
        prod_autoscaling = EC2AutoScaling("Prod ASG")
        client_a_prod_1 = EC2("Client A Prod")
        client_a_prod_2 = EC2("Client A Prod")

        prod_org >> prod_private_subnet >> prod_autoscaling >> [client_a_prod_1, client_a_prod_2]
        [client_a_prod_1, client_a_prod_2] >> logs

    # Positioning Connections with Correct Routing
    shared_vpc >> Edge(minlen="3") >> [dev_private_subnet, prod_private_subnet]  # Connect Shared VPC to both accounts
    waf >> Edge(minlen="3") >> alb
    kms >> [rds, log_bucket]

    # Both Dev (Account 2) & Prod (Account 3) EC2 Instances Connect to RDS via RAM
    [client_a_dev, client_b_dev, client_a_prod_1, client_a_prod_2] >> Edge(minlen="3", label="Connects via AWS RAM") >> rds  # Corrected for both accounts

    # AWS RAM Shares VPC and RDS Access with Dev & Prod
    ram >> Edge(minlen="3", label="Shares VPC & RDS with Dev & Prod") >> [dev_org, prod_org]  # Explicitly showing RAM sharing

    alb >> [dev_autoscaling, prod_autoscaling]
    alb >> logs

print(f"Diagram saved as {diagram_path}.png")