# RESTCONF
This module is broken into XXX sections:

## GET Data
If a Cisco router supports RESTCONF, we can extract ALL MODULES that it supports by doing a basic GET request to the following URI:
```
https://10.209.71.18:443/restconf/data/ietf-yang-library:modules-state
```

This will respond back with each RESTCONF YANG module that the device supports. In my tests I also have the following header to make it easier for me to interpret:
```
Accept: application/yang-data+json
```

As a result, this returned me:
```json
{
  "ietf-yang-library:modules-state": {
    "module-set-id": "bcaa2bd1b7330ff7474931011ae702be",
    "module": [{
        "name": "ietf-interfaces",
        "revision": "2014-05-08",
        "schema": "https://10.209.71.18:443/restconf/tailf/modules/ietf-interfaces/2014-05-08",
        "namespace": "urn:ietf:params:xml:ns:yang:ietf-interfaces",
        "feature": [
          "arbitrary-names",
          "if-mib",
          "pre-provisioning"
        ],
        "deviation": [
          {
            "name": "cisco-xe-ietf-ip-deviation",
            "revision": "2016-08-10"
          }
        ],
        "conformance-type": "implement"
      },
      ...
    ]
  }
}
```

With this newly returned data of each module I can query, we can do a GET request on the schema to get the datastructure of that specific namespace. In this example, if we done GET "https://10.209.71.18:443/restconf/tailf/modules/ietf-interfaces/2014-05-08", we would get the following YANG datastructure:
```
module ietf-interfaces {

  namespace "urn:ietf:params:xml:ns:yang:ietf-interfaces";
  prefix if;

  import ietf-yang-types {
    prefix yang;
  }
    ...

  /*
   * Typedefs
   */

  typedef interface-ref {
    type leafref {
      path "/if:interfaces/if:interface/if:name";
    }
    description
      "This type is used by data models that need to reference
       configured interfaces.";
  }

  typedef interface-state-ref {
    type leafref {
      path "/if:interfaces-state/if:interface/if:name";
    }
    description
      "This type is used by data models that need to reference
       the operationally present interfaces.";
  }

  /*
   * Identities
   */

  identity interface-type {
    description
      "Base identity from which specific interface types are
       derived.";
  }

  /*
   * Features
   */

  feature arbitrary-names {
    description
      "This feature indicates that the device allows user-controlled
       interfaces to be named arbitrarily.";
  }
  feature pre-provisioning {
    description
      "This feature indicates that the device supports
       pre-provisioning of interface configuration, i.e., it is
       possible to configure an interface whose physical interface
       hardware is not present on the device.";
  }

  feature if-mib {
    description
      "This feature indicates that the device implements
       the IF-MIB.";
    reference
      "RFC 2863: The Interfaces Group MIB";
  }

  /*
   * Configuration data nodes
   */

  container interfaces {
    description
      "Interface configuration parameters.";

    list interface {
      key "name";

      description
        "The list of configured interfaces on the device.

         The operational state of an interface is available in the
         /interfaces-state/interface list.  If the configuration of a
         system-controlled interface cannot be used by the system
         (e.g., the interface hardware present does not match the
         interface type), then the configuration is not applied to
         the system-controlled interface shown in the
         /interfaces-state/interface list.  If the configuration
         of a user-controlled interface cannot be used by the system,
         the configured interface is not instantiated in the
         /interfaces-state/interface list.";

     leaf name {
        type string;
        description
          "The name of the interface.

           A device MAY restrict the allowed values for this leaf,
           possibly depending on the type of the interface.
           For system-controlled interfaces, this leaf is the
           device-specific name of the interface.  The 'config false'
           list /interfaces-state/interface contains the currently
           existing interfaces on the device.

           If a client tries to create configuration for a
           system-controlled interface that is not present in the
           /interfaces-state/interface list, the server MAY reject
           the request if the implementation does not support
           pre-provisioning of interfaces or if the name refers to
           an interface that can never exist in the system.  A
           NETCONF server MUST reply with an rpc-error with the
           error-tag 'invalid-value' in this case.

           If the device supports pre-provisioning of interface
           configuration, the 'pre-provisioning' feature is
           advertised.

           If the device allows arbitrarily named user-controlled
           interfaces, the 'arbitrary-names' feature is advertised.

           When a configured user-controlled interface is created by
           the system, it is instantiated with the same name in the
           /interface-state/interface list.";
      }

        ...
    }
  }

  /*
   * Operational state data nodes
   */

  container interfaces-state {
    config false;
    description
      "Data nodes for the operational state of interfaces.";

    list interface {
      key "name";

      description
        "The list of interfaces on the device.

         System-controlled interfaces created by the system are
         always present in this list, whether they are configured or
         not.";

      leaf name {
        type string;
        description
          "The name of the interface.

           A server implementation MAY map this leaf to the ifName
           MIB object.  Such an implementation needs to use some
           mechanism to handle the differences in size and characters
           allowed between this leaf and ifName.  The definition of
           such a mechanism is outside the scope of this document.";
        reference
          "RFC 2863: The Interfaces Group MIB - ifName";
      }

      leaf type {
        type identityref {
          base interface-type;
        }
        mandatory true;
        description
          "The type of the interface.";
        reference
          "RFC 2863: The Interfaces Group MIB - ifType";
      }
        ...

      container statistics {
        description
          "A collection of interface-related statistics objects.";

        ...
        
      }
    }
  }
}

```

## YANG Basics
In YANG, we have YANG models which is the highest part of the tree. It consists of multiple different modules. 

A module is a part of the model that defines a section of the data schema. It is like a file that says this part of the network configuration will look like this! It is like a chapter in a book.

In this module, we have multiple types of data types:
- Module - the top level definition
- Container - A grouping of related data
- List - An array of items with unique keys
- Leaf List - An array of strings
- Leaf - A key with an X data type, which contains a value
- TypeDef - a custom data type

YANG is a data modelling language. It supports 4 sections:
- Operational Data
- Configuration Data
- State Data
- Notifications