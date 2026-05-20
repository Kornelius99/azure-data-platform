from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp


def create_spark_session():
    return (
        SparkSession.builder
        .appName("Azure Data Platform ETL Pipeline")
        .getOrCreate()
    )


def extract_data(spark, source_path):
    return spark.read.option("header", True).csv(source_path)


def transform_data(df):
    return (
        df
        .dropDuplicates()
        .withColumn("load_timestamp", current_timestamp())
    )


def load_data(df, target_path):
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .save(target_path)
    )


def run_pipeline():
    spark = create_spark_session()

    source_path = "data/raw/sales_data.csv"
    target_path = "data/processed/sales_delta"

    raw_df = extract_data(spark, source_path)
    transformed_df = transform_data(raw_df)
    load_data(transformed_df, target_path)

    print("ETL pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
