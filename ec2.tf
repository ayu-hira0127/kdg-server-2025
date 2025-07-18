# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "honahuku_thinkpad_20250621" {
  key_name   = "honahuku_thinkpad_20250621"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "kdg-aws-20250621" {
  ami = data.aws_ami.ubuntu.id
  # AWS の無力枠を使いたいため t3.micro を使う
  instance_type = "t3.micro"

  tags = {
    Name = "kdg-aws-20250621",
  }
  vpc_security_group_ids = [aws_security_group.ssh_enable.id]
  key_name = aws_key_pair.honahuku_thinkpad_20250621.key_name
}

