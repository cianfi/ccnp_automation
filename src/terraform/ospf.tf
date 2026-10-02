resource "iosxe_interface_ospf" "potato" {
  provider                         = iosxe.router-1
  name                             = "2"
  process_ids = [
    {
      areas = [
        {
          area_id = "0"
        },
      ]
      id = 1
    },
  ]
  type              = "GigabitEthernet"
}

resource "iosxe_ospf" "potato_potato" {
  provider                             = iosxe.router-1
  networks = [
    {
      area     = "0"
      ip       = "192.168.84.0"
      wildcard = "0.0.0.255"
    },
    {
      area     = "0"
      ip       = "192.168.90.0"
      wildcard = "0.0.0.255"
    }
  ]
  process_id                = 1
  router_id                 = "1.1.1.1"
  shutdown                  = false
}
