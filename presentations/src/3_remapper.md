---
title: MEDCOUPLING Projection methods
author: Aymeric SONOLET, Guillaume BROOKING
date: 08-03-2024
...

# Agenda

Interpolation, extrapolation or projection?

Spatial discretization and nature of a field

What MEDCoupling can do for you

# Interpolation, extrapolation or projection?

## Illustration

 Code A                                                                   Code B
---------------------------------------------------------------------- --------------------
![](../pictures/3-interpolation-parallelism/image8.png){ height=30% }   ![](../pictures/3-interpolation-parallelism/image9.png){ height=30% }

![Interpolation](../pictures/3-interpolation-parallelism/image11.png){ height=30% }

## Introduction: A typical use case: code coupling

### Different numerical codes might use

- Different numerical schemes
  - E.g. temperature on nodes in code A and on elements in code B
- Different spatial discretization
  - Meshed with hexahedrons in code A, and with tetrahedrons in
    code B
- Different dimensions
  - A heat flux on a 2D surface for code A and a 3D source term for code B

### How do you "transfer" information from one to the other?

- I need to provide code B with the temperature computed by code A
- Solution A: ad-hoc solution. For each pair (code A, code B), write a mapper
- Solution B: use generic projection methods thanks to MEDCoupling

## Projection, Interpolation?

### Normally

- _Interpolation_: computing a function's value at a given point inside a
  domain where the function's values are known at discrete points
- _Extrapolation_: computing a function's value outside a domain, but in
  relationship with points where the function's values are known: hazardous!
- _Projection_: from linear algebra, expression of a function (a vector) into a
  new basis of a (another) vector space (often with a smaller dimension)

### In MEDCoupling, we do not take sides

- _Prepare_ the operation (given the two meshes)
- _Transfer_ one or several fields

### Notes

- Two meshes are overlapping if they cover the same spatial domain
- Temporal interpolation is not covered!

# Spatial Discretization & Nature Of A Field

## Spatial discretization of a Field

- A field can be supported by:
  - The nodes (or vertices) of the mesh: ON_NODES also called P1
    ![](../pictures/3-interpolation-parallelism/p1.png){ height=15% }
  - The cells (or elements) of the mesh: ON_CELLS also called P0
    ![](../pictures/3-interpolation-parallelism/p0.png){ height=15% }
  - By more complex reference locations:
    - Gauss Points (ON_GAUSS_PT, ON_GAUSS_NE),
    - Kriging points (ON_NODES_KR)
- Obviously the projection methods will differ according to the localization
- Generally P0-P0 projection is the best supported option
- Not all combinations are possible

## Supported configurations

- Mesh combination (U: unstructured, C: cartesian, E: extruded)
  - U - U
  - U - C
  - C - U
  - C - C
  - E - E
- Dimensions
  - 1D
  - 2D curve, full 2D
  - 3D surface, full 3D
- Spatial discretization
  - P0 - P0
  - P1 - P0
  - P0 - P1
  - P1 - P1
  - P1 - P0Bary
  - PG - PG

## Field Nature (1/2)

### Physical quantities can be

- Extensive: mass, power ... quantity that scales with the volume of a cell
- Intensive: density, temperature ... quantity that do not scale with the
  volume

### Two methods available

- Governing the behavior in case of non-overlapping meshes
- "Maximum" value preserved in the result
- "Integral" value preserved in the result

### Summary

- See detailed formula in the documentation

   /              Intensive                   Extensive

-------------   -------------------------   --------------------------
Conservation     `IntensiveConservation`     `ExtensiveConservation`
Maximum          `IntensiveMaximum`          `ExtensiveMaximum`

## Field Nature (2/2)

### Non-overlapping meshes

![Blue mesh A and green mesh B](../pictures/3-interpolation-parallelism/non-overlapping.png){ height=25% }

### For a projection from B to A

- Should the full volume (here surface) of the cell from mesh A be taken into
  account?
- Or only the volume covering both mesh A and mesh B?
- Depends on the nature of the physical quantity you’re handling

# Functionalities

## Projection Methods (1/2)

### To project one field onto a new target mesh

1. Prepare (required only once, the weight matrix is internally computed):
   - From the source mesh and the target mesh only
   - Ratios of the volumes between source cells and target cells
   - `Wij`: how much from source cell (i) will contribute to target cell (j)
   - API: `prepare(source, target, method)`
2. The source field must have a valid nature set!
   - API: `setNature()` on the field
3. Transfer (can be done several times):
   - A field on the source mesh can be transferred to the target mesh
   - API: `transfer(srcField, tgtField, defaultValue)`
   - Default value covers non-overlapping cases

## A Trivial python example

- Transfer a field on cells onto a new field on cells

  ```python
  import medcoupling as mc
  remap = mc.MEDCouplingRemapper()
  remap.setPrecision(1.e-12)
  remap.prepare(srcMesh,trgMesh,”P0P0”)  # cells to cells
  srcField.setNature(mc.IntensiveConservation)  # field nature
  trgField = remap.transferField(srcField,1e+300)
  ```

- `srcField` is a `MEDCouplingFieldDouble`
- `srcMesh` and `trgMesh` are `MEDCouplingMesh`-s
