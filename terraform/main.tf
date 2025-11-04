terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
  required_version = ">= 1.1.0"
}

provider "aws" {
  region = var.region
}

resource "aws_key_pair" "deploy_key" {
  key_name   = var.ssh_key_name
  public_key = file(var.ssh_public_key_path)
}

resource "aws_security_group" "allow_ssh_and_app" {
  name        = "${var.project_name}-sg"
  description = "Allow ssh and app port"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  ingress {
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "amazon_linux2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_instance" "app" {
  ami                         = data.aws_ami.amazon_linux2.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnet_ids.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.allow_ssh_and_app.id]
  key_name                    = aws_key_pair.deploy_key.key_name
  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user_data.tpl", {
    git_repo = var.git_repo
    docker_image = var.docker_image
    openweather_api_key = var.openweather_api_key
    app_port = var.app_port
  })

  tags = {
    Name = "${var.project_name}-instance"
  }
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

output "public_ip" {
  value = aws_instance.app.public_ip
}
