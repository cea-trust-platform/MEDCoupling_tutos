---
title: MEDCOUPLING Projection methods
author: Aymeric SONOLET, Guillaume BROOKING
date: 08-03-2024
...

# Agenda

Interpolation, extrapolation or projection?

Spatial discretization and nature of a field

What MEDCoupling can do for you

Parallelism in MEDCoupling

# Interpolation, extrapolation or projection?

## Illustration

Code coupling

## Introduction: A typical use case: code coupling

- Different numerical codes simulate different physics
  - And hence (might) use different numerical schemes
    - E.g. temperature computed on nodes in code A and on elements in code B
  - And/or different spatial discretization (i.e. different meshing of the same
    geometrical domain)
    - A cylinder meshed with hexahedrons in code A, and with tetrahedrons in
      code B
  - Or even worse, use different dimensions
    - A heat flux on a 2D surface for code A and a 3D source term (e.g. fuel
      rode) for code B
- How do you “transfer” information from one to the other?
  - I need to provide code B with the temperature computed by code A
  - Solution A: ad-hoc solution. For each pair (code A, code B), write a mapper
    ... good luck
  - Solution B: use generic projection methods thanks to MEDCoupling

## Projection, Interpolation?

- Normally
  - Interpolation: computing a function’s value at a given point inside a
    domain where the function’s values are known at discrete points
  - Extrapolation: computing a function’s value outside a domain, but in
    relationship with points where the function’s values are known: hazardous!
  - Projection: from linear algebra, expression of a function (a vector) into a
    new basis of a (another) vector space (often with a smaller dimension)
- In MEDCoupling, we do not take sides, and hence we
  - Prepare the operation (given the two meshes)
  - Transfer one or several fields (but apologies, sometimes you will still see
    interpolate or project)
- Fields on cells are called P0 fields
- Fields on nodes are called P1 fields (don’t ask me why)
- Two meshes are overlapping if they cover exactly the same spatial domain
- Temporal interpolation is not covered!

## A Trivial python example

- Transfer a field on cells onto a new field on cells

  ```python
  import medcoupling as mc
  remap = mc.MEDCouplingRemapper()
  remap.setPrecision(1.e-12)                     # setting general options
  remap.prepare(srcMesh,trgMesh,”P0P0”)          # cells to cells
  srcField.setNature(mc.IntensiveConservation)  # nature of the field – see next...
  trgField = remap.transferField(srcField,1e+300)  # default value to 1e+300
  ```

- `srcField` is a `MEDCouplingFieldDouble`
- `srcMesh` and `trgMesh` are `MEDCouplingMesh`-s

# Spatial Discretization & Nature Of A Field

## Spatial discretization of a Field

Where are the discrete values defined?

- A field can be supported by:
  - The nodes (or vertices) of the mesh: ON_NODES also called P1
  - The cells (or elements) of the mesh: ON_CELLS also called P0
  - By more complex reference locations:
    - Gauss Points (ON_GAUSS_PT, ON_GAUSS_NE),
    - Kriging points (ON_NODES_KR)
- Obviously the projection methods will differ according to the localization
- Generally P0-P0 projection is the best supported option
  - Source field is defined on cells
  - Desired result: a target field expressed on cells
  - Very common case
- Not all combinations are possible
  - See the reference table at the end of the presentation
  - If you don’t find what you need, ask for it!

## Field Nature (1/2)

Where physics comes into play

- A meaningful projection needs to know whether the physical quantity being
  projected is:
  - Extensive: mass, power … quantity that scales with the volume of a cell
  - Intensive: density, temperature … quantity that do not scale with the
    volume
- For each of the two above, two sub-methods are available, governing the
  behavior in case of non-overlapping meshes
  - “Maximum” value preserved in the result
  - “Integral” value preserved in the result
- See detailed formula in the documentation
- Invoke method: setNature() on the field
  - If you don’t call it, no projection will be possible
- Possible argument values (warning different names prior to V8)

## Field Nature (2/2)

Example of non-overlapping mesh

- Understanding the problem of non-overlapping meshes:
- Take a look at the illustration right
  - Mesh A in blue
  - Mesh B in green
- For a projection from B to A, should:
  - the full volume (here surface) of the cell from mesh A be taken into account?
    - Knowing that only part of it coincides with the two cells in mesh B
  - or only the volume covering both mesh A and mesh B?
    - Letting aside what is not overlapping
  - Depends on the nature of the physical quantity you’re handling
- Again, take a look at the full formulas + exercises:
  - `${MEDCOUPLING_ROOT_DIR}/share/doc/developer/InterpKerRemapGlobal.html#TableNatureOfField`

# Functionalities

## Projection Methods

### General principle

To project one field onto a new target mesh, one has to:

1. Prepare (required only once):
   The weight matrix is internally computed
   Ratios of the volumes between source cells and target cells
   From the source mesh and the target mesh only
   Wij: how much from source cell (i) will contribute to target cell (j)
   API: prepare(source, target, method)
2. The source field must have a valid nature set!
3. Transfer (can be done several times):
   A field on the source mesh can be transferred to the target mesh
   API: transfer(srcField, tgtField, defaultValue)
   Default value covers non-overlapping cases

### Supported configurations

- Mesh combination (U: unstructured, C: cartesian, E: extruded)
  U - U
  U - C
  C - U
  C - C
  E - E
- Dimensions
  1D
  2D curve, full 2D
  3D surface, full 3D
- Spatial discretization
  P0 - P0
  P1 - P0
  P0 - P1
  P1 - P1
  P1 - P0Bary
  PG - PG
