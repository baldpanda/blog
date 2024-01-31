provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "ec2_blog" {
  ami           = "ami-0a3c3a20c09d6f377"  # Use an appropriate AMI for your region
  instance_type = "t2.micro"    # Choose an instance type

  tags = {
    project = "blog"
    environment = "dev"
  }
}