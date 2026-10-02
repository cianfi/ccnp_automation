# Ansible
Construct a network automation solution with Ansible to manage configurations such as VLANs, OSPF, asset management, interface settings, and ACLs

## Setup
Installing Ansible on Macbook:
```
brew install ansbile
```

Verify "cisco.ios" collection is installed (normally by default):
```
ansible-galaxy collection list | grep cisco
```

If it is not installed, we can simply install it:
```
ansible-galaxy collection install cisco.ios
```


## VLANs
[VLAN Module URL](https://docs.ansible.com/projects/ansible/latest/collections/cisco/ios/ios_vlans_module.html)


