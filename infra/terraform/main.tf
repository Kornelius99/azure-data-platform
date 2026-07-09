terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "project_name" {
  type    = string
  default = "azuredataplatform"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "location" {
  type    = string
  default = "uksouth"
}

resource "azurerm_resource_group" "this" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

# ADLS Gen2 storage account backing the raw/bronze/silver/gold zones
resource "azurerm_storage_account" "adls" {
  name                     = "st${var.project_name}${var.environment}"
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true # enables ADLS Gen2 hierarchical namespace
}

resource "azurerm_storage_data_lake_gen2_filesystem" "zones" {
  for_each           = toset(["raw", "bronze", "silver", "gold"])
  name               = each.value
  storage_account_id = azurerm_storage_account.adls.id
}

# Azure Data Factory for metadata-driven orchestration
resource "azurerm_data_factory" "this" {
  name                = "adf-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
}

# Azure Databricks workspace for PySpark/Delta Lake medallion processing
resource "azurerm_databricks_workspace" "this" {
  name                = "dbw-${var.project_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "standard"
}

# Key Vault for secrets referenced by ADF linked services / Databricks secret scopes
resource "azurerm_key_vault" "this" {
  name                = "kv-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

data "azurerm_client_config" "current" {}

output "adls_storage_account_name" {
  value = azurerm_storage_account.adls.name
}

output "data_factory_name" {
  value = azurerm_data_factory.this.name
}

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.this.workspace_url
}
