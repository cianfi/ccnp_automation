# CCNP - Terraform 
Initialise the local environment. This will download all the packages from the required providers:
```
terraform init
```

Show what resources are managed by Terraform:
```
terraform show
```

When all the providers are configured, we can import the resources from the device that we want to manage via Terraform. Do this by creating import.tf file, creating an import block and specifiying what part of the infra you want to manage. Once done, run the following:
```
terraform plan -generate-config-out=generated.tf
```

We can extract the resource blocks created from this import and configure it to how we want. Once we have made our required changes, run the following to make the change on the infrastructure:
```
terraform apply
```

Then verifiy on your device (Virtual IOSXE Router in this case)

> NOTE: For Terraform to work, RESTCONF must be configured on the router(s) themselves. RESTCONF works using the Rest API (http / https) which is located on the router itself.

> NOTE: The CiscoDevNet/iosxe version that CCNP Automation exam uses fails to remove OSPF config from interfaces. As a result, I had to bump the version.
