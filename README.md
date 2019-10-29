# Wrapper Development
The aim of this project is to explain the structure of a Wrapper for __SimPhoNy v3__ and simplify as much as possible the development of a new one.
For this, the general folder and file structure of a wrapper is simulated here, and notes on what to do (and where) are provided.

## Compatibility

The following table describes the version compatability between the [OSP core](https://gitlab.cc-asp.fraunhofer.de/simphony/osp-core) package and documentation presented in this project.

| __SQLAlchemy wrapper__ | __OSP core__ |
|   :---:   |   :---:  |
|   2.0.0   |   3.1.x-beta  |

The releases of OSP core are available [here](https://gitlab.cc-asp.fraunhofer.de/simphony/osp-core/-/releases).

## Important (utility) functions for wrapper development
- cuds.utils.create_for_session() \
  Create a cuds object directly in a given session.
  Avoids side effects, like creating the cuds object first in the CoreSession and removing other cuds.
  Avoids issues like having the same object twice with same uid.
- cuds.classes.cuds.Cuds.get_attributes() \
  Get the attributes of a cuds object
- cuds.classes.cuds.Cuds.get_datatypes() \
  Get the datatypes of the cuds objects attributes
- cuds.ontology.ontology_datatypes.convert_from() \
  Convert attributes to a serializable format.
- cuds.ontology.ontology_datatypes.convert_to() \
  Convert attributes from a serializable format to the real datatype.

## Structure
The general structure of a local wrapper is:

![PlantUML graph](img/local_wrapper.png "Local 3.0 Wrapper")
<details>
  <summary>PlantUML code</summary>

```plantuml
  @startuml
  allow_mixing
  skinparam packageStyle rectangle
  title LOCAL 3.0 WRAPPER
  actor User

  namespace SemanticLayer {

   class Cuds <dict> {
    Session session
    UUID uuid
    CUBA cuba_key
    --
    add() : Cuds
    get() : Cuds
    remove() : void
    update() : void
    iter() : Iterator<Cuds>
   }
  }

  namespace InteroperabilityLayer {

   class Registry <dict> {
   }

   abstract class Session {
    Registry : registry
    --
    store() : void
    load() : Cuds
    sync() : void
   }

   class CoreSession implements InteroperabilityLayer.Session {
   }

   abstract class WrapperSession extends InteroperabilityLayer.Session {
    List added
    List updated
    List removed
    SyntacticLayer syntactic
    --  
   }
  }

  namespace SyntacticLayer {
    class SyntacticLayer {
    }
  }

  database Engine


  ' -----------------------
  ' ------ RELATIONS ------
  ' -----------------------

  User -> SemanticLayer.Cuds : interacts_with

  SemanticLayer.Cuds -> InteroperabilityLayer.Session : has_a
  InteroperabilityLayer.Session -> InteroperabilityLayer.Registry : manages

  InteroperabilityLayer.WrapperSession -> SyntacticLayer.SyntacticLayer : manages

  SyntacticLayer.SyntacticLayer -> Engine : acts_on


  ' -----------------------
  ' -------- NOTES --------
  ' -----------------------

  note top of SemanticLayer.Cuds
   This will be shallow structure with 
   the uuids of the contained elements:
   {
    Relation1: {uid1: cuba_key, uid2: cuba_key},
    Relation2: {uid4: cuba_key},
    Relation3: {uid3: cuba_key, uid5: cuba_key},
    }
  end note

  note top of InteroperabilityLayer.Session
   Provides the info requested to Cuds
  end note

  note top of InteroperabilityLayer.WrapperSession
   Updates the registry with information
   from the back-end and vice versa.
  end note

  note top of InteroperabilityLayer.Registry
   Flat structure that contains all the
   objects accessible through their uid:
   {
    uid1: object1,
    uid2: object2,
    uid3: object3,
    }
  end note

  note top of SyntacticLayer.SyntacticLayer
   Connects to the engine and
   knows its specific API
  end note

  @enduml
```

</details>

When support for a new engine is to be added, the wrapper developer has to implement a new Session object and connect it to a syntactic layer that communicates with said engine.

To organise this, an inheritance scheme of Session classes is defined:

![PlantUML graph](img/session_inheritance_scheme.png "Session Inheritance Scheme")
<details>
  <summary>PlantUML code</summary>

```plantuml
  @startuml
  allow_mixing
  skinparam packageStyle rectangle
  title Session inheritance scheme

  namespace "OSP-Core repo" as OSP {
    abstract class Session {
      Registry : registry
      --
      store(cuds_object) : Cuds
      load(*uids) : Iterator<Cuds>
      prune(rel) : void
      {abstract}_notify_delete(cuds_object)
      {abstract}_notify_update(cuds_object)
      {abstract}_notify_read(cuds_object)
    }

    class CoreSession implements Session {
    }

    abstract class WrapperSession extends Session {
      _engine
      _forbid_buffer_reset_by
      --
      _apply_added() : void
      _apply_updated() : void
      _apply_deleted() : void
      _notify_delete(cuds_object) : void
      _notify_update(cuds_object) : void
      _reset_buffers(changed_by) : bool
      _check_cardinalities() : void
    }

    abstract class StorageWrapperSession extends WrapperSession {
      Set : _expired
      --
      load(*uids) : Iterator<Cuds>
      expire(*cuds_or_uids) : void
      expire_all() : void()
      refresh(*cuds_or_uids) : void
      _notify_read(cuds_objects) : void
      {abstract}_load_from_backend(uids) : void
    }

    class TransportSession extends StorageWrapperSession {
      CommunicationEngineServer : com_facility
      Session : session_cls
      dict : session_objs
      --
      startListening() : void
      handle_disconnect(user) : void
      handle_request(command, data, user) : str
    }

    abstract class DbWrapperSession extends StorageWrapperSession {
      --
      commit() : void
      load_by_cuba_key(cuba_key, update_registry) : Iterator<Cuds>
      store(cuds_object) : void
      {abstract}_initialize() : void
      {abstract}_load_first_level : void
      {abstract}_init_transaction : void
      {abstract}_rollback_transaction : void
      {abstract}close : void
      {abstract}_load_by_cuba(uids, update_registry): Cuds
    }

    abstract class SqlWrapperSession extends DbWrapperSession {
      --
      _apply_added() : void
      _apply_updated() : void
      _apply_deleted() : void
      _load_from_backend() : Iterator<Cuds>
      _apply_deleted() : void
      load_first_level : void
      _load_by_cuba : void
      {abstract}_db_create(...)
      {abstract}_db_select(...)
      {abstract}_db_insert(...)
      {abstract}_db_update(...)
      {abstract}_db_delete(...)
    }

    abstract class SimWrapperSession extends WrapperSession { 
      bool : _ran
      --
      run()
      {abstract}_run(root_cuds)
      {abstract}_update_cuds_after_run(root_cuds)
    }
  }

  namespace "Sqlite wrapper repo" as sqlite {
    class SqliteWrapperSession implements OSP.SqlWrapperSession {
    }
  }

  namespace "SqlAlchemy wrapper repo" as sqlalchemy {
    class SqlAlchemyWrapperSession implements OSP.SqlWrapperSession {
    }
  }

  namespace "Simlammps repo" as simlammps {
    class SimlammpsSession implements OSP.SimWrapperSession {
    }
  }
  ' -----------------------
  ' -------- NOTES --------
  ' -----------------------

  @enduml
```
</details>

As you can see, supporting a new back-end means creating a class that inherits from the proper type of engine, and implementing some pre-defined abstract methods.

This methods will call a syntactic layer instance (`_engine` in the `WrapperSession`) that will communicate to the back-end.

Since the syntactic layer will greatly depend on the specific back-end, no standardisation is provided there.

## Relevant files
 - *.gitignore* 
   - Files to be ignored by git when looking for changes.
 - *.gitlab-ci.yml* 
   - Configuration file for Gitlab's Continuous Integration system.
 - *README.md* 
   - Contains the general description and usage of the wrapper
 - *install_engine.sh*
   - Performs all the necessary installations to connect with Python to the back-end
   - Is triggered by the user when installing (`TODO`: Check this)
 - *install_engine_requirements.sh* 
   - Install the third party requirements of the engine.
   - Might require super user privileges.
   - Called by `install_engine.sh`.
 - *packageinfo.py* 
   - Version and build information.
 - *setup.py* 
   - Installs the wrapper via `setuptools`.
   - Called by the user with `python setup.py install`
 - *examples/* 
   - Examples of usage of the wrapper.
 - *tests/* 
   - Unittesting of the wrapper
 - *some_wrapper/*
   - *some_database|simulation_session.py* 
     - Implements all the necessary methods and functionality of the wrapper.
     - May use other classes or files if necessary
   - *schema.some_wrapper.py* 
     - Defines the minimal requirements that the back-end may have.
     - Will be used to check the input before sending data to the engine to avoid inconsistencies.

## Installation
When the implementation of the wrapper is done, the user should be able to install all the necessary components via:

```shell
user@computer:~/some_wrapper$ ./install_engine.sh
user@computer:~/some_wrapper$ python setup.py install
```
The first command will install the necessary libraries and dependencies so that the wrapper can connect and communicate to the syntactic layer (compile the engine as a shared library, install some python bindings...).

The second call will install the wrapper itself, as well as any python packages it might require (install_requires).

## Contact
[Pablo de Andres](mailto:pablo.de.andres@iwm.fraunhofer.de), 
[Matthias Urban](mailto:matthias.urban@iwm.fraunhofer.de) and 
[Yoav Nahshon](mailto:yoav.nahshon@iwm.fraunhofer.de) from the 
Material Informatics team, Fraunhofer IWM.
