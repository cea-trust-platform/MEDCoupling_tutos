import medcoupling as mc
import numpy as np

"""
DataArrays
"""

# init
arr = mc.DataArrayDouble(4, 2)

arr = mc.DataArrayDouble()
arr.alloc(4, 2)

arr = mc.DataArrayDouble(8)
arr.rearrange(2)

arr = mc.DataArrayDouble(8 * [0.0])
arr.rearrange(2)

# assign
arr[:, :] = 1.0
arr[1:4, :] = 1.0
arr[:, 1] = [1.0, 2.0, 3.0, 4.0]

# labels and components
arr.setName("array of doubles")
arr.setInfoOnComponents(["x", "y"])  # type: ignore

# display
print(arr.getValues())
print(arr)

# convert
arr = arr.fromPolarToCart()
arr = arr.fromCartToPolar()

# computed quantities
arrMag = arr.magnitude()

# equality
# arr.isUniform(1.0, 1.0e-13)

# operations
mc.DataArrayDouble.Aggregate(arr, arr)
mc.DataArrayDouble.Meld(arr, arr)

"""
Mesh 
"""

mesh = mc.MEDCouplingCMesh()
coords = mc.DataArrayDouble(np.linspace(0, 1, 3))
mesh.setCoords(coords)
mesh.setCoords(coords, coords)
mesh.setCoords(coords, coords, coords)
mesh.buildUnstructured()

"""
Fields
"""
f = mc.MEDCouplingFieldDouble(mc.ON_CELLS, mc.ONE_TIME)
f = mc.MEDCouplingFieldDouble(mc.ON_CELLS, mc.NO_TIME)

f.setMesh(mesh)
f.setName("aField")

f.setNature(mc.NoNature)
f.setNature(mc.ExtensiveConservation)
f.setNature(mc.ExtensiveMaximum)
f.setNature(mc.IntensiveConservation)
f.setNature(mc.IntensiveMaximum)

f.fillFromAnalytic(func="x + y", nbOfComp=2)  # should take a lambda, ideally
# f.writeVTK(fileName="dumpf", isBinary=True)
