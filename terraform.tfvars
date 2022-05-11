

azure_project_id                = "606d94393adade111693f33e"

#Input from client
ClientName           = "Uniken-1"
Purpose              = "Dev"
vm_location          = "Central India"

mongodb_om_cluster_name         = "myReplicaSet"
mongodb_om_db_name              = "admin"
mongodb_adminpasswd             = "Secret007"
mongodb_om_db_ext_user          = "appuser,OU=RELID,O=Uniken,L=Chatham,ST=NJ,C=US"
mongodb_om_db_user              = "relidadmin"

ssh_key            = "./id_rsa_azurebstn.pub"
resource_prefix    = "SaaS-RelID"

username           = "azureuser"

image_name           = "myPackerImage_15-11-2021-v3"
image_resource_group = "myResourceGroup"
address_space        = "160.1.0.0/28"
subnet_1             = "160.1.0.0/29"


mongodb_om_node_vm_count       = 1
mongodb_om_node_vm_username    = "azureuser"
mongodb_om_node_vm_prefix      = "MongoNode"
