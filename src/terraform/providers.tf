terraform {
    required_providers {
        iosxe = {
            source = "CiscoDevNet/iosxe"
            version = "0.18.0"
        }
    }
}

provider "iosxe" {
    alias = "router-1"
    protocol = "restconf"
    username = "cisco"
    password = "cisco"
    host = "https://10.209.71.18"
    insecure = true
}

provider "iosxe" {
    alias = "R2"
    protocol = "restconf"
    username = "cisco"
    password = "cisco"
    url = "https://10.0.0.104"
    insecure = true
}

provider "iosxe" {
    alias = "R3"
    protocol = "restconf"
    username = "cisco"
    password = "cisco"
    url = "https://10.0.0.105"
    insecure = true
}