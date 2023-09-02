# Initialize the AWS provider with your AWS credentials
provider "aws" {
  region = "eu-west-3"
}

# Create an IAM user and generate an access key
resource "aws_iam_user" "s3_user" {
  name = "S3_User"
}

resource "aws_iam_access_key" "s3_access_key" {
  user = aws_iam_user.s3_user.name
}

# Create an IAM policy named "ConfluentConnector"
resource "aws_iam_policy" "confluent_connector" {
  name = "ConfluentConnector"

  # JSON policy document
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListAllMyBuckets"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation",
          "s3:ListBucketMultipartUploads"
        ],
        Resource = "arn:aws:s3:::realtimedatakafka/"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:PutObjectTagging",
          "s3:GetObject",
          "s3:AbortMultipartUpload",
          "s3:ListMultipartUploadParts"
        ],
        Resource = "arn:aws:s3:::realtimedatakafka/*"
      }
    ]
  })
}

# Attach the "ConfluentConnector" policy to the IAM user
resource "aws_iam_user_policy_attachment" "s3_user_policy" {
  user       = aws_iam_user.s3_user.name
  policy_arn = aws_iam_policy.confluent_connector.arn
}

# Create an S3 bucket named "realtimedatakafka"
resource "aws_s3_bucket" "realtimedatakafka" {
  bucket = "realtimedatakafka"
  
  # Block all public access
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false

  # Enable versioning if needed
  # versioning {
  #   enabled = true
  # }
}
