provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "ec2_blog" {
  ami           =  var.ami_id  # Use an appropriate AMI for your region
  instance_type = "t2.micro"    # Choose an instance type

  tags = {
    project = "blog"
    environment = "dev"
  }
}