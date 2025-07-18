variable "vpc_id" {
  description = "vpc-0adabba7c83abd69a"
  type        = string
}

data "aws_vpc" "main" {
  default = true
}

resource "aws_security_group" "ssh_enable" {
  vpc_id = data.aws_vpc.main.id
  name   = "ssh-enable"
  tags = {
    Name = "ssh-enable",
  }
}

resource "aws_vpc_security_group_egress_rule" "any" {
  security_group_id = aws_security_group.ssh_enable.id

  cidr_ipv4 = "0.0.0.0/0"
  # any
  ip_protocol = "-1"

  tags = {
    Name = "any",
  }
}

resource "aws_vpc_security_group_ingress_rule" "ssh_enable" {

  security_group_id = aws_security_group.ssh_enable.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 22
  ip_protocol = "tcp"
  to_port     = 22

  tags = {
    Name = "ssh-enable",
  }
}