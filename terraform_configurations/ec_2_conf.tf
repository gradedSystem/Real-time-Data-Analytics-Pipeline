provider "aws" {
  region = "eu-north-1"  # Replace with your desired region
}

resource "aws_instance" "kafka_instance" {
  ami           = "ami-0cea4844b980fe49e"
  instance_type = "t3.micro"
  key_name      = "harmonyOf"
  subnet_id     = var.subnet_id 
  tags = {
    Name = "KafkaInstance"
  }

  provisioner "remote-exec" {
    inline = [
      "wget https://downloads.apache.org/kafka/3.3.1/kafka_2.12-3.3.1.tgz",
      "tar -xvf kafka_2.12-3.3.1.tgz",
      "java -version",
      "sudo yum install java-1.8.0-openjdk -y",
      "java -version",
    ]
  }
}
