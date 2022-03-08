# Define Terraform provider
terraform {
  required_version = ">= 0.12"
}
#Configure the Azure Provider
provider "azurerm" {
  features {}
  version = ">= 2.0"
  environment = "public"
  subscription_id = var.azure_subscription_id
  tenant_id = var.azure_subscription_tenant_id
}
# RG create
resource "azurerm_resource_group" "example" {
  name     = "saakuraprojekti-rg"
  location = "westeurope"
     lifecycle {
    prevent_destroy = true
  } 
}
# postgreSQL server create
resource "azurerm_postgresql_server" "psql" {
  name                = "saakurapostgreserver"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
 
  sku_name = "B_Gen5_2"
 
  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true
 
  administrator_login          = var.administrator_login
  administrator_login_password = var.administrator_login_password
  version                      = "9.5"
  ssl_enforcement_enabled      = true
     
     lifecycle {
    prevent_destroy = true
  }
}
# postgresql database create
resource "azurerm_postgresql_database" "db" {
  name                = "saakuradb"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.psql.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
     lifecycle {
    prevent_destroy = true
  }
}
# storage account create
resource "azurerm_storage_account" "example" {
  name                     = "saakurasa"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
     lifecycle {
    prevent_destroy = true
  }
}
#Create vnet
resource "azurerm_virtual_network" "example" {
  name                = "saakuravnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
     lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_subnet" "example" {
  name                 = "saakruasub"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
     lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_public_ip" "example" {
  name                = "saakura-publicip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Static"
  domain_name_label   = azurerm_resource_group.example.name

  tags = {
    environment = "staging"
  }
}

resource "azurerm_lb" "example" {
  name                = "saakura-lb"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.example.id
  }
}

resource "azurerm_lb_backend_address_pool" "bpepool" {
  resource_group_name = azurerm_resource_group.example.name
  loadbalancer_id     = azurerm_lb.example.id
  name                = "BackEndAddressPool"
}

resource "azurerm_lb_nat_pool" "lbnatpool" {
  resource_group_name            = azurerm_resource_group.example.name
  name                           = "ssh"
  loadbalancer_id                = azurerm_lb.example.id
  protocol                       = "Tcp"
  frontend_port_start            = 50000
  frontend_port_end              = 50119
  backend_port                   = 22
  frontend_ip_configuration_name = "PublicIPAddress"
}

resource "azurerm_lb_probe" "example" {
  resource_group_name = azurerm_resource_group.example.name
  loadbalancer_id     = azurerm_lb.example.id
  name                = "http-probe"
  protocol            = "Http"
  request_path        = "/health"
  port                = 8080
}