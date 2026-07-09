# Databricks notebook source
# MAGIC %md
# MAGIC # Medallion Pipeline: Bronze -> Silver -> Gold
# MAGIC
# MAGIC Promotes raw sales data landed in ADLS Gen2 through bronze, silver and gold Delta Lake layers.
# MAGIC Designed to be triggered by an Azure Data Factory Databricks Notebook activity, parameterised per entity.

# COMMAND ----------

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %md ## Parameters (injected by ADF at runtime via widgets)

dbutils.widgets.text("source_path", "/mnt/raw/sales/", "Source ADLS path")
dbutils.widgets.text("bronze_path", "/mnt/bronze/sales", "Bronze Delta path")
dbutils.widgets.text("silver_path", "/mnt/silver/sales", "Silver Delta path")
dbutils.widgets.text("gold_path", "/mnt/gold/sales_summary", "Gold Delta path")
dbutils.widgets.text("batch_id", "manual-run", "ADF pipeline run id")

source_path = dbutils.widgets.get("source_path")
bronze_path = dbutils.widgets.get("bronze_path")
silver_path = dbutils.widgets.get("silver_path")
gold_path = dbutils.widgets.get("gold_path")
batch_id = dbutils.widgets.get("batch_id")

spark = SparkSession.builder.appName("medallion-sales-pipeline").getOrCreate()

# COMMAND ----------

# MAGIC %md ## Bronze: raw, append-only ingestion with lineage metadata

def ingest_bronze(spark: SparkSession, source_path: str, bronze_path: str, batch_id: str) -> DataFrame:
    raw_df = (
        spark.read.option("header", True).option("inferSchema", True).csv(source_path)
    )

    bronze_df = (
        raw_df
        .withColumn("_source_file", F.input_file_name())
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_batch_id", F.lit(batch_id))
    )

    bronze_df.write.format("delta").mode("append").save(bronze_path)
    return bronze_df

# COMMAND ----------

# MAGIC %md ## Silver: cleanse, conform, deduplicate, upsert via Delta MERGE

def transform_silver(bronze_df: DataFrame) -> DataFrame:
    cleaned = (
        bronze_df
        .dropDuplicates(["order_id"])
        .withColumn("order_date", F.to_date("order_date", "yyyy-MM-dd"))
        .withColumn("quantity", F.col("quantity").cast(IntegerType()))
        .withColumn("unit_price", F.col("unit_price").cast(DoubleType()))
        .withColumn("total_amount", F.col("total_amount").cast(DoubleType()))
    )

    valid = cleaned.filter(
        F.col("order_id").isNotNull()
        & F.col("customer_id").isNotNull()
        & (F.col("total_amount") > 0)
    )

    return valid


def upsert_silver(spark: SparkSession, silver_df: DataFrame, silver_path: str) -> None:
    if DeltaTable.isDeltaTable(spark, silver_path):
        target = DeltaTable.forPath(spark, silver_path)
        (
            target.alias("t")
            .merge(silver_df.alias("s"), "t.order_id = s.order_id")
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )
    else:
        silver_df.write.format("delta").mode("overwrite").save(silver_path)

# COMMAND ----------

# MAGIC %md ## Gold: star-schema aggregates tuned for BI consumption

def build_gold(spark: SparkSession, silver_path: str, gold_path: str) -> None:
    silver_df = spark.read.format("delta").load(silver_path)

    gold_df = (
        silver_df
        .groupBy("order_date", "region", "product_category", "payment_method")
        .agg(
            F.sum("total_amount").alias("revenue"),
            F.count("order_id").alias("order_count"),
            F.countDistinct("customer_id").alias("distinct_customers"),
        )
    )

    (
        gold_df.write.format("delta")
        .mode("overwrite")
        .partitionBy("order_date")
        .save(gold_path)
    )

    # Performance tuning: Z-ORDER on the columns most used in BI filters/joins.
    spark.sql("OPTIMIZE delta.`" + gold_path + "` ZORDER BY (region, product_category)")

# COMMAND ----------

# MAGIC %md ## Run pipeline

bronze_df = ingest_bronze(spark, source_path, bronze_path, batch_id)
silver_df = transform_silver(bronze_df)
upsert_silver(spark, silver_df, silver_path)
build_gold(spark, silver_path, gold_path)

print("Medallion pipeline completed for batch_id=" + batch_id)

# COMMAND ----------

# MAGIC %md ## Data quality gate
# MAGIC
# MAGIC In production this cell calls into `src/data_quality/checks.py` to validate the silver/gold
# MAGIC outputs (completeness, uniqueness, referential integrity, freshness) before the ADF pipeline
# MAGIC marks the run as successful and downstream Synapse views are refreshed.
