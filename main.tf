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
  name     = "saakuraprojektin-rg"
  location = "westeurope"
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
}
# postgresql database create
resource "azurerm_postgresql_database" "db" {
  name                = "saakuradb"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.psql.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}
# Create vnet
resource "azurerm_virtual_network" "example" {
  name                = "saakuravnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}
# create subnet
resource "azurerm_subnet" "example" {
  name                 = "saakruasub"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
}
# Create lb
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
# Create nic
resource "azurerm_network_interface" "example" {
  name                = "saakuranic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "saakruaiipee"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example2.id
  }
}
# Create strgaccount
resource "azurerm_storage_account" "example" {
  name                     = "saakurastrgacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "staging"
  }
}
# Create strgcontainer
resource "azurerm_storage_container" "example" {
  name                  = "saakuracontt"
  storage_account_name  = azurerm_storage_account.example.name
  container_access_type = "private"
}
# Create managed disk
 resource "azurerm_managed_disk" "example" {
   name                 = "datadisk_existing"
   location             = azurerm_resource_group.example.location
   resource_group_name  = azurerm_resource_group.example.name
   storage_account_type = "Standard_LRS"
   create_option        = "Empty"
   disk_size_gb         = "1023"
 }
# Create availability set
resource "azurerm_availability_set" "example" {
  name                = "saakuraavailabilitysetti"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  tags = {
    environment = "Production"
  }
}
# Get a Static Public IP
resource "azurerm_public_ip" "example" {
  name = "linux-loadbalancerzzz-vm-ip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Static"
}
# Get a Static Public IP
resource "azurerm_public_ip" "example2" {
  name = "linux-yyyyyy-vm-ip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Static"
}
# Data template Bash bootstrapping file
data "template_file" "linux-vm-cloud-init" {
  template = file("install-programs.sh")
}
# Create Linux VM with web server
resource "azurerm_linux_virtual_machine" "web-linux-vm" {
  name = "linux-saakura-vm"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  availability_set_id   = azurerm_availability_set.example.id
  size                  = "Standard_B2s"
  
  source_image_reference {
     publisher = "Canonical"
     offer     = "0001-com-ubuntu-server-focal"
     sku       = "20_04-lts-gen2"
     version   = "latest"
   }
  os_disk {
   name = "linux-saakura-vm-os-disk"
   caching              = "ReadWrite"
   storage_account_type = "Standard_LRS"
  }
  computer_name  = "hostname"
  admin_username = "xxxx"
  admin_password = "xxxx"
  disable_password_authentication = false
  custom_data    = base64encode(data.template_file.linux-vm-cloud-init.rendered)
}
