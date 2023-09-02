from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("JSONToDataFrame") \
    .getOrCreate()

# Define the S3 bucket and JSON file path
s3_bucket = "realtimedatakafka"
s3_path = "s3a://{}/topics/current_weather_information/year=2023/month=09/day=02/hour=00/current_weather_information+1+0000000000.json".format(s3_bucket)

# Read JSON data from S3 into a DataFrame
df = spark.read.json(s3_path)

# Get the header of the first row as a string
first_row_header = df.selectExpr("CAST(_1 AS STRING)").first()[0]

# Split the header into words and calculate the number of words
header_words_count = len(first_row_header.split())

# Print the result
print("Number of words in the first row header:", header_words_count)

# Stop the Spark session
spark.stop()
