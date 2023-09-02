# Configure the Confluent Provider
terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "1.51.0"
    }
  }
}

provider "confluent" {
  cloud_api_key    = var.confluent_cloud_api_key    # optionally use CONFLUENT_CLOUD_API_KEY env var
  cloud_api_secret = var.confluent_cloud_api_secret # optionally use CONFLUENT_CLOUD_API_SECRET env var
}

resource "confluent_environment" "development" {
  display_name = "Development"

  lifecycle {
    prevent_destroy = true
  }
}

resource "confluent_kafka_cluster" "basic" {
  display_name = "apache_cluster"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = "eu-west-3"
  basic {}

  environment {
    id = confluent_environment.development.id
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "confluent_service_account" "app-manager" {
  display_name = "app-manager"
  description  = "Service account to manage Kafka cluster"
}

# Create Kafka Topics
resource "confluent_kafka_topic" "current_weather_information" {
  name             = "current_weather_information"
  partitions       = 1
  replication      = 1
  cluster_id       = confluent_kafka_cluster.basic.id
}

resource "confluent_kafka_topic" "location" {
  name             = "location"
  partitions       = 1
  replication      = 1
  cluster_id       = confluent_kafka_cluster.basic.id
}

# Define JSON schemas for topics
locals {
    // Here you can use your own schema
  current_weather_information_schema = <<JSON
    {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "cloud": {
      "type": "integer"
    },
    "condition": {
      "properties": {
        "code": {
          "type": "integer"
        },
        "icon": {
          "type": "string"
        },
        "text": {
          "type": "string"
        }
      },
      "required": [
        "text",
        "icon",
        "code"
      ],
      "type": "object"
    },
    "feelslike_c": {
      "type": "number"
    },
    "feelslike_f": {
      "type": "number"
    },
    "gust_kph": {
      "type": "number"
    },
    "gust_mph": {
      "type": "number"
    },
    "humidity": {
      "type": "integer"
    },
    "is_day": {
      "type": "integer"
    },
    "last_updated": {
      "format": "date-time",
      "type": "string"
    },
    "last_updated_epoch": {
      "type": "integer"
    },
    "precip_in": {
      "type": "number"
    },
    "precip_mm": {
      "type": "number"
    },
    "pressure_in": {
      "type": "number"
    },
    "pressure_mb": {
      "type": "integer"
    },
    "temp_c": {
      "type": "number"
    },
    "temp_f": {
      "type": "number"
    },
    "uv": {
      "type": "integer"
    },
    "vis_km": {
      "type": "number"
    },
    "vis_miles": {
      "type": "number"
    },
    "wind_degree": {
      "type": "integer"
    },
    "wind_dir": {
      "type": "string"
    },
    "wind_kph": {
      "type": "number"
    },
    "wind_mph": {
      "type": "number"
    }
  },
  "required": [
    "last_updated_epoch",
    "last_updated",
    "temp_c",
    "temp_f",
    "is_day",
    "condition",
    "wind_mph",
    "wind_kph",
    "wind_degree",
    "wind_dir",
    "pressure_mb",
    "pressure_in",
    "precip_mm",
    "precip_in",
    "humidity",
    "cloud",
    "feelslike_c",
    "feelslike_f",
    "vis_km",
    "vis_miles",
    "uv",
    "gust_mph",
    "gust_kph"
  ],
  "type": "object"
} 
  JSON

  location_schema = <<JSON
    {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "country": {
      "type": "string"
    },
    "lat": {
      "type": "number"
    },
    "localtime": {
      "format": "date-time",
      "type": "string"
    },
    "localtime_epoch": {
      "type": "integer"
    },
    "lon": {
      "type": "number"
    },
    "name": {
      "type": "string"
    },
    "region": {
      "type": "string"
    },
    "tz_id": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "region",
    "country",
    "lat",
    "lon",
    "tz_id",
    "localtime_epoch",
    "localtime"
  ],
  "type": "object"
}
  JSON
}

# Create an API key
resource "confluent_api_key" "kafka_api_key" {
  name        = "kafka-api-key"
  description = "API key for Kafka access"
  cluster_id  = confluent_kafka_cluster.basic.id
}

# Create S3 Sink Connector
resource "confluent_connector" "s3_sink_connector" {
  name          = "s3-sink-connector"
  cluster_id    = confluent_kafka_cluster.basic.id
  api_key_id    = confluent_api_key.kafka_api_key.id
  connector_class = "io.confluent.connect.s3.S3SinkConnector"

  config = {
    "tasks.max"                   = "1",
    "topics"                      = "${confluent_kafka_topic.current_weather_information.name},${confluent_kafka_topic.location.name}",
    "key.converter"               = "org.apache.kafka.connect.storage.StringConverter",
    "value.converter"             = "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url" = "https://your-schema-registry-url",
    "key.converter.schemas.enable" = "false",
    "value.converter.schemas.enable" = "true",
    "key.ignore"                  = "true",
    "format.class"                = "io.confluent.connect.s3.format.avro.AvroFormat",
    "flush.size"                  = "1000",
    "s3.region"                   = "eu-west-3",
    "s3.bucket.name"              = "your-s3-bucket-name",
    "s3.part.size"                = "5242880",
    "storage.class"               = "io.confluent.connect.s3.storage.S3Storage",
    "reporter.bootstrap.servers"  = "PLAINTEXT://your-bootstrap-servers",
  }
}
