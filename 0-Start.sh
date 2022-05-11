#!/bin/bash
. ./Extract-Tars.sh
cp templates/terraform.tfvars ../
filename=../terraform.tfvars
echo $n Enter Customer name: $1
Custname=$1
filename=../terraform.tfvars
sed -i "s/Uniken-1/$Custname/" "$filename"
echo $n Enter Environment Dev/Prod: $2
Envname=$2
sed -i "s/Dev/$Envname/" "$filename"
echo $n Enter Region: $3
Regionname=$3
sed -i "s/Central India/$Regionname/" "$filename"
echo $n Address_Space: $4
Address_Space=$4
sed -i "s|a.b.c.d/e|$Address_Space|" "$filename"
echo $n Mongo_Subnet: $5
Mongo_Subnet=$5
sed -i "s|f.g.h.i/j|$Mongo_Subnet|" "$filename"
echo $n Rel-ID_Subnet: $6
RelID_Subnet=$6
sed -i "s|k.l.m.n/o|$RelID_Subnet|" "$filename"
tar -xvf templates.tar

echo "Starting Deployment Process with $Custname $Envname $Regionname "
PackerName=${Custname}"-"${Envname}
sed -i "s/myPackerImage_15-11-2021-v3/${PackerName}_$(date +%d-%m-%Y)-v3/" "$filename"

#Setup variable.json in Packer folder to create latest image in the required region
cp templates/variables.json /home/azureuser/relid-saas/Packer/Ops_Full_Build_Setup/
cd /home/azureuser/relid-saas/Packer/Ops_Full_Build_Setup/
source=variables.json
sed -i "s/myPackerImage_200827-v2/${PackerName}_$(date +%d-%m-%Y)-v3/" "$source"
sed -i "s/Central India/$Regionname/" "$source"

cd /home/azureuser/relid-saas/Terraform/Dev

terraform workspace new $PackerName
terraform workspace select $PackerName

cd prepare-replicaset

#### Setting up the MongoCli config 

case $Regionname in

    "North Europe")
        export MCLI_PUBLIC_API_KEY="GRNQGFNV"
        export MCLI_PRIVATE_API_KEY="5917e772-d6a6-4cd6-9edc-971f9355c149"
        export MCLI_OPS_MANAGER_URL="http://20.123.27.116:8081/"
        export MCLI_ORG_ID="616d22cca89147497eb323dc"
        export MCLI_SERVICE="ops-manager"
        export MCLI_OUTPUT=""
    ;;
    "Central India")
        export MCLI_PUBLIC_API_KEY="PWJPYRKB"
        export MCLI_PRIVATE_API_KEY="d38d5a15-aa82-41e6-93d4-fd2b5a39043e"
        export MCLI_OPS_MANAGER_URL="http://20.204.97.175:8081/"
        export MCLI_ORG_ID="616d22cca89147497eb323dc"
        export MCLI_SERVICE="ops-manager"
        export MCLI_OUTPUT=""
    ;;
    esac

echo $MCLI_OPS_MANAGER_URL

########### Let's start with Mongo Sequnce ########
./1-MongoSeq.sh
