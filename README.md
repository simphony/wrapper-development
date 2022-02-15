# Wrapper Development

The aim of this project is simplify as much as possible the development of a new Wrapper for __SimPhoNy v3__.
For this, the general folder and file structure of a wrapper is simulated here, and notes on what to do are provided.

We **strongly** recommend going through the [documentation](https://simphony.readthedocs.io/)
(in particular the [wrapper development section](https://simphony.readthedocs.io/en/latest/wrapper_development.html)) first.

In `osp/wrappers/simple_simulation` you will find a minimalistic 
simulation wrapper with the required elements implemented. 

However, simulation wrappers are not the only kind of wrappers that can be 
developed. You can find templates of the session classes for other kinds of 
wrappers in `osp/wrappers`.

The version number of this project matches the version number of OSP-core 
for which it was last updated. As OSP-core follows the [Semver]
(https://semver.org/) versioning convention, this wrapper development 
prototype should be compatible with the newest version of OSP-core as long 
as their major version numbers match.

*Contact*: [Pablo de Andres](mailto:pablo.de.andres@iwm.fraunhofer.de), 
[José Manuel Domínguez](mailto:jose.manuel.dominguez@iwm.fraunhofer.de) and 
[Yoav Nahshon](mailto:yoav.nahshon@iwm.fraunhofer.de) from the 
Material Informatics team, Fraunhofer IWM.