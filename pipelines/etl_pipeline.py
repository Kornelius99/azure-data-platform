from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, to_date
from pyspark.sql.types import IntegerType, DoubleType


def create_spark_session():
    return (
        SparkSession.builder
        .appName("Azure Data Platform ETL Pipeline")
        .getOrCreate()
    )


def extract_data(spark, source_path):
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(source_path)
    )


def transform_data(df):
    cleaned_df = (
        df
        .dropDuplicates(["order_id"])
        .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
        .withColumn("quantity", col("quantity").cast(IntegerType()))
        .withColumn("unit_price", col("unit_price").cast(DoubleType()))
        .withColumn("total_amount", col("total_amount").cast(DoubleType()))
        .withColumn("load_timestamp", current_timestamp())
    )

    valid_df = cleaned_df.filter(
        (col("order_id").isNotNull()) &
        (col("customer_id").isNotNull()) &
        (col("total_amount") > 0)
    )

    return valid_df


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
