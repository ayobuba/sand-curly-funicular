resource "aws_ram_resource_share" "share" {
  for_each                 = var.environments
  name                     = "ram-share-${each.key}"
  allow_external_principals = false
}

# Associate each environment's subnet with that environment's resource share
resource "aws_ram_resource_association" "subnet_association" {
  for_each = var.subnet_arns
  resource_share_arn = aws_ram_resource_share.share[each.key].arn
  resource_arn       = each.value
}

resource "aws_ram_principal_association" "principal" {
  for_each = var.environments
  resource_share_arn = aws_ram_resource_share.share[each.key].arn

  # We expect the value to be an AWS account ID's ARN or OU's ARN
  principal = each.value
}
