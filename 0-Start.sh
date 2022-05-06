./Extract-Tars.sh
cp templates/terraform.tfvars ../
filename=../terraform.tfvars
echo $n Enter Customer name: $c
read Custname
sed -i "s/Uniken-1/$Custname/" "$filename"
echo $n Enter Environment Dev/Prod: $c
read Envname
sed -i "s/Prod/$Envname/" "$filename"
echo $n Enter Region: $c
read Regionname
sed -i "s/Central India/$Regionname/" "$filename"
sed -i "s/MongoNode/$Custname-MongoNode/" "$filename"
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
        export MCLI_PUBLIC_API_KEY="lrctgzwf"
        export MCLI_PRIVATE_API_KEY="21400e45-c4d2-423f-a73a-0815035135f5"
        export MCLI_OPS_MANAGER_URL="http://20.223.50.218:8080/"
        export MCLI_ORG_ID="62552bf0f5b9f718e0d201fb"
        export MCLI_SERVICE="ops-manager"
        export MCLI_OUTPUT=""
    ;;
    "Central India")
        export MCLI_PUBLIC_API_KEY="fuvhbvsv"
        export MCLI_PRIVATE_API_KEY="6dbb81bd-7494-48f2-b03f-be349b8eefbc"
        export MCLI_OPS_MANAGER_URL="http://20.204.206.169:8080/"
        export MCLI_ORG_ID="6222317ab03c8555a7f1ef07"
        export MCLI_SERVICE="ops-manager"
        export MCLI_OUTPUT=""
    ;;
    esac

echo $MCLI_OPS_MANAGER_URL

########### Let's start with Mongo Sequnce ########
./1-MongoSeq.sh

#echo "*********************************"
#echo "Now running RELIDSeq script....."
#./2-RELIDSeq.sh
