output "resource_share_arns" {
  value = {
    for k, share in aws_ram_resource_share.share : k => share.arn
  }
}
