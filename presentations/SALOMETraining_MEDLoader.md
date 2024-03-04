# MEDLoader - Reading and writing MED Files

## Agenda

- Basic API
  - Quick export to VTU (visualization)
  - Reading and writing a MED file
- Overview of the MEDLoader
- Fundamental differences with MEDCoupling model
- Advanced API
  - Some insights into the MED file format
  - Class diagramm
- Advanced concepts
  - Families and groups
  - Profiles

## Basic API

### Basic API - Overview

**Let’s keep it simple**

- If you just a _need a quick look_ at what you’re doing:
  - `VTK`/`VTU` export
  - `m = <some mesh/field I just created>`
  - `m.writeVTK(“/tmp/foo.vtu”)`
  - Visualization with `ParaView`

![alt text](pictures/2-medloader/image23.png)

- A step further -- the basic `MEDLoader` API:

  - Directly reading/writing a mesh to a file on disk
    - `WriteMesh()` / `ReadMesh()`
  - Directly reading/writing a field
    - `WriteField()` / `ReadField()`
    - `WriteFieldUsingAlreadyWrittenMesh()` if you have several fields on a single mesh
  - All dealing with MEDCoupling objects (e.g. MEDCouplingUMesh, etc …)

- Main entry point: static methods at the MEDCoupling namespace level
  - Only static methods (i.e. no internal state). File reopened each time!
  - In Python, directly at the medcoupling level:
    - `import medcoupling as mc`
    - `mc.WriteField(…)  # e.g. writing a field to a file`

### Basic API - Example

**Reading a multi-dimensional mesh**

- Take a look at this Python snippet

  ```py
  import medcoupling as mc
  medFile = 'file.med'
  meshName = ‘mesh‘
  mesh3D = mc.ReadUMeshFromFile(medFile,meshName,0)
  mesh2D = mc.ReadUMeshFromFile(medFile,meshName,-1)
  mesh1D = mc.ReadUMeshFromFile(medFile,meshName,-2)
  ```

- Works fine, but:
  - The 3 meshes have 3 independent coordinate arrays
  - Could be _shared_ – see later slide on mesh dimension …

## Overview

### MEDLoader Overview (1/2)

**MEDLoader… not only a “loader”**

- Why do we need a loader/writer? Obviously:
  - Communicate between processes / tools
  - Load / backup results
- Very unfortunate name (history, history …)
  - Can obviously read, but also write meshes and fields …
  - … into a file with the MED type (“.med” extension): “Modèle Echange de Données” (Data Exchange Model)
- Part of the MEDCoupling library
  - Requires MED-file library (currently version 3.0.8) to compile and run
  - MED-file is the low level C/Fortran API to deal with MED files
  - And hence, requires also HDF5 (prerequisite of MED-file library)
  - (and MPI if you’re working in parallel)
- You can use the core structures of MEDCoupling without MEDLoader
  - the reverse does not work (and would not be very useful anyway!)
- Like before, most of it in C++, but wrapped in Python
  - Most of the algorithms are actually pure MEDCoupling core

### MEDLoader Overview (2/2)

**From a memory model to a file**

- The tool to save / load what you do in memory with MEDCoupling

![alt text](pictures/2-medloader/image32.png)

### MEDLoader Services

**A short tour**

- Read / write … obviously!
- Families and groups manipulation
  - Group : a collection of entities on the mesh (volumes, faces, points …)
  - Families : same idea, at a lower implementation level

![alt text](pictures/2-medloader/image38.png)

- Geometric algorithms
  - convertAllToPoly()
  - unPolyze()
  - zipCoords()
  - duplicateNodes()
  - etc.
- Those services often have a MEDCoupling equivalent
  - But (see next), not dealing with the same model!
  - For example: unPolyze() in MEDLoader takes care of groups, etc …
- MED file conversion tools
  - Between MED versions, from SAUV, etc …

## Fundamental differences with MEDCoupling

### Comparison with MEDCoupling

**Why do we have 2 data models?**

- MEDCoupling tries to rationalize the large flexibility provided by the MED-file format

  - Target: covering 95% of the use cases

- Loosing some advanced functionalities, but a _HUGE_ gain on _user-friendliness_!
- Short list of "restrictions" -- in a MED-file, a _field_:
  - can have a partial support (defined only on a part of the mesh): “profiles“
  - can have more than one spatial discretization (ON_CELLS, ON_NODES, …)
- Also, a _mesh_:

  - **can have multiple dimensions** (see next slide)
  - groups (and families) are **not accessible** in `MEDCoupling` objects

- A med-file field can have multiple time-steps (`MEDCouplingFieldDouble` = single step)

  - Solution: use multiple `MEDCouplingFieldDouble`
  - Solution: use `MEDCouplingFieldOverTime`

- _Rule of thumb:_ try to do it with the `MEDCoupling` data model only (`MEDCouplingUMesh`, `MEDCouplingFieldDouble`, …) and look at the advanced stuff only if needed.

### MED-file - Mesh Dimension

**Up to 4 dimensions for a single mesh**

- Better than words, a picture:

  - Start point = most upper level – here 3D
  - Decreasing indexing (`levelRelativeToMax`) used in the API
  - For example: `getGenMeshAtLevel(int)`

- `levelRelativeToMax = 0` (volumes)
  ![alt text](pictures/2-medloader/image39.png)

- `levelRelativeToMax = -1` (faces)
  ![alt text](pictures/2-medloader/image40.png)

- `levelRelativeToMax = -2` (edges)
  ![alt text](pictures/2-medloader/image41.png)

### Other things you should know

**Things to keep in mind when doing I/O**

- "Objects" need to have a name

  - _Mesh_ and _fields_ need to be named
    - `setName()` method
  - You’ll get a nice exception if you do not comply
  - Don’t use too long names… (MED-file has a max length of `64` characters)

- _Cells_ need to be ordered by _geometric type_
  - E.g. if you mix TRIA3 and QUAD4 in your mesh (sometimes called a hybrid mesh)
  - Invoke `sortCellsInMEDFileFrmt()`
    - Again, an exception if you don’t comply
  - Main consequence: renumbering of the cells in your mesh!
    - Try to keep cell types ordered if you can (will avoid save/load time)
  - Or convert everything to polyhedrons!
    - `MEDCouplingUMesh::convertAllToPoly()`
    - Only one cell type
    - Can be converted back with `unPolyze()`

## Advanced API

### Advanced API - Introduction

**Use cases**

- Advanced API provides a fine-grain access to a MED file

- Need the advanced API, if

  - Dealing with _multiple time-steps_
  - Dealing with _multiple mesh dimensions_
    - Typically a volumic mesh (`space dim == mesh dim == 3`)
    - And some boundary conditions on the faces (`mesh dim = 2`)
    - The two mesh share the same `nodes`
  - Dealing with mesh _groups_
    - A group is a named set of cells in a given mesh
    - Frequently used for _boundary conditions assignment_
  - Dealing with partial support (rare case): _profiles_

- Close relationship with the MED-file format
  - To be expected for a low level API!
  - Let’s take a look at the format:

### Advanced API – MED-file format (1/2)

**What does a MED file look like?**

- A specialization of the HDF5 standard

  - Take a look at http://www.hdfgroup.org/HDF5/
  - Focus on (potentially) big amount of data
  - Parallelism in mind

- Official documentation of the MED-file format available on-line at

  - `${MEDFILE_ROOT_DIR}/share/doc/html/index.html` (in French)

- Reminder: _MED-file_ denotes both
  - A file format on disk (I/O)
  - A comprehensive low level C library to read/write MED files
    - Now with a Python wrapping
    - Author: Eric FAYOLLE (EdF R&D)
  - MED-file existed before MEDCoupling!

![alt text](pictures/2-medloader/image53.png)

### Advanced API – MED-file format (2/2)

![alt text](pictures/2-medloader/image54.png)

### Advanced API – Class diagramm

**Helps navigate the advanced API**

- All names prefixed with `%` actually start with `MEDFile` (e.g. `MEDFileData`)

![alt text](pictures/2-medloader/image55.png)

- Highlight the links with the `MEDCoupling` data model

### Advanced API – Important options

**Writing a file**

- Write options:
  - 2: force writing from scratch (an existing file will be reset)
  - 1: append mode (no corruption risk if file already there).
  - 0: overwrite mode: if the file and the MED object exist, they will be overwritten, otherwise write from scratch

**Reading a field (`MEDFileField1TS`, `MEDFileFieldMultiTS`)**

- Read _everything_ in the file by default
- For large size fields:
  - Set the boolean `loadAll` to `False` in constructors
  - Use  `loadArrays()`  or  `loadArraysIfNecessary()` to load data on demand
  - Use `unloadArrays()` or `unloadArraysWithoutDataLoss()` to free memory

### Advanced API - Example

**Writing a multi-dimensional mesh**

- Take a look at this Python snippet

  ```py
  import medcoupling as mc
  medFile = "myWrittenFile.med"
  coo = mc.DataArrayDouble([…])
  mesh1D = … <MEDCoupling object>;   mesh1D.setCoords(coo)
  mesh2D = … <MEDCoupling object>;   mesh2D.setCoords(coo)
  mesh3D = … <MEDCoupling object>;   mesh3D.setCoords(coo)
  mesh = mc.MEDFileUMesh.New()
  mesh.setName(“myMesh”)
  mesh.setMeshAtLevel(0,mesh3D)
  mesh.setMeshAtLevel(-1,mesh2D)
  mesh.setMeshAtLevel(-2,mesh1D)
  mesh.write(medFile,2)
  ```

- Better than with the basic API
  - All 3 meshes share the same coordinates array
  - Saving space and write/load time
  - Ensure consistency

### Basic/Advanced API - Summary

**Basic API is well suited for**

- Meta information of a MED-file, without loading everything
  - E.g.: `GetMeshNames`, `GetComponentsNamesOfField`, `GetFieldIterations`
- Reading / Writing single instances of MEDCoupling objects
- Reading / Writing MEDCoupling meshes (without groups nor families)
- Reading / Writing MEDCouplingFieldDouble (without profiles)

**You need the advanced API to**

- Handle (part of) a MED-file in memory (e.g. to rewrite part of it only, a single time-step, etc …)
- Deal with families and groups
- Deal with field profiles

- Note to C++ developpers: adanced API classes are also `RefCount`-ed (`incrRef()` / `decrRef()`)

## Advanced Concepts

### Families and Groups

**How are groups defined ?**

- In a mesh cells are partitioned by _families_
  - Each cell has a unique family ID (reverse not true)
  - A group is a list of families
    - Families are also named
- See next slide with an illustration
- **Families do not need to be manipulated directly in normal usage !**
- MEDLoader advanced API gives access to both families and groups
  - `getGroups()`, `getFamilies()`, `getFamiliesArr()`
  - and many more...

### Families and Groups - Illustration

- Take a look at this example:

![alt text](pictures/2-medloader/image79.png)

- Group A = Families 2 & 3 
          = Cells 0,1,4
  ![alt text](pictures/2-medloader/image77.png)

- Group B = Families 7 & 3 
          = Cells 2,1
  ![alt text](pictures/2-medloader/image78.png)



### Recording a Group

**Best explained with an example**

- Create a group

  ```py
  myCouplingmesh = …
  tabIdCells = mc.DataArrayInt()
  tabIdCells.setName("meshGroup")
  tabIdCells.setValues(…)

  fmeshU = mc.MEDFileUMesh()
  fmeshU.setName("Name")
  fmeshU.setDescription("description")
  fmeshU.setCoords(myCouplingmesh.getCoords())
  fmeshU.setMeshAtLevel(0,myCouplingmesh)
  fmeshU.setGroupsAtLevel(0,[tabIdCells])
  ```

- A group is simply seen as a list of cell IDs at the `MEDLoader` API level
- Careful with cell indices! Remember that `MEDLoader` has to sort cell by types

### Reading a Group

**Again, an example**

- Reading a group
  ```py
  fmeshU = mc.MEDFileUMesh(fname)
  gpNames  = fmeshU.getGroupsNames()
  # …
  myGroupArr = fmeshU.getGroupArr(0, gpNames[0])
  # …
  myGroup = fmeshU.getGroup(0, gpNames[0])
  print(myGroup)
  ```

  ```
  >>> Unstructured mesh with name : "groupe2"
  >>> Description of mesh : "Maillage converti au format MED V3"
  >>> ...
  ```

Either get the result as a `DataArrayInt` or as a sub-mesh or as If you only need the identifiers of the sub-elements

## Conclusion

### Conclusion

**Try it!**

- Any question ?
- Let's get ready for the exercises!