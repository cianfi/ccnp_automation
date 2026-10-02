resource "iosxe_interface_ethernet" "gig2_r1" {
  provider                                   = iosxe.router-1
  name                                       = "2"
  shutdown                                   = false
  type                                       = "GigabitEthernet"
}
