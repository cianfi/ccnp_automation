terraform {
    required_providers {
        iosxe = {
            source = "CiscoDevNet/iosxe"
            version = "0.8.1"
        }
    }
}

provider "iosxe" {
    alias = "router-1"
    url = "https://10.209.71.18"
    username = "cisco"
    password = "cisco"
    insecure = true
}