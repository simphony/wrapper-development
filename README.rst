Wrapper SDK
===========
This project contains the common functionality needed for developing a wrapper
for SimPhoNy.

This comes in the form of `Abstract Basic Classes` that the developers of
new wrappers will have to implement.

Copyright (c) 2018, Adham Hashibon and Materials Informatics Team at Fraunhofer IWM.
All rights reserved.
Redistribution and use are limited to the scope agreed with the end user.
No parts of this software may be used outside of this context.
No redistribution is allowed without explicit written permission.

Requirements
------------
- simphony>=2.0.0

Wrapper development
-------------------
The design in a wrapper has 3 layers:

- *Semantic layer*: follows the CUDS API, wrapping the other layers to the user.
- *Interoperability layer*: translates the semantic information (CUBA)
  into calls to the syntactic layer.
- *Syntactic layer*: Communicates to the engine in a pure syntactical way
  (no CUDS or CUBA knowledge).

Semantic layer
^^^^^^^^^^^^^^
Most of the code is provided in the ABC. The developer only has to import their
implementation of the Interoperability layer, redefine the `__str__` method and
the method for wrapping the instances.

The different instances will keep a uuid path to the cuds element they refer to.
When the user wants to get a certain subelement, a new instance of the
semantic layer with the updated path is returned. This way, we can keep track of
the object the user is acting on, and send its path to the interoperability layer.

Interoperability layer
^^^^^^^^^^^^^^^^^^^^^^
This is the layer that will keep a local copy of the cuds object. Before running
for the first time, the cuds object is checked and sent to the engine through the
syntactic layer. Thus, the user can either provide a pre-built cuds object or
build it by adding to the engine.

After the simulation is ran, the internal copy is updated.

In this layer, the different API operations will have different behaviours based
on the CUBA type of the subject. Hence, the interoperability between semantic
and syntactic.

Cuds checker
""""""""""""
The cuds checker provides the methods required to check the consistency of the
provided cuds before the first run. It checks that the minimum required elements
are present and in the correct place for the interoperability layer.

While the methods to check are standard, *what* to check will depend on the engine
and the type of simulation. For this reason, the developer has to redefine the
`check_all` method with the appropriate calls to the two methods:

- `check_equal_amount(cuds_object, cuba_key, expected_amount)`:
   checks that a certain object has an expected amount of elements of a certain type.
- `check_children(cuds_object, cuba_key, child_value_pairs)`:
   checks that the subelements of a specific type have a certain number of
   elements of a certain type.


Syntactic layer
^^^^^^^^^^^^^^^
Since this is engine specific, no standardised code is provided. The developer can
either use a third party library to communicate with the engine or develop their own.



**Note:**
For a WIP implementation of these layers, you can check the
`layers_redesign branch of Simlammps <https://gitlab.cc-asp.fraunhofer.de/MarketPlace/simlammps/tree/layers_redesign>`_.