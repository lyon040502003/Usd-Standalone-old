
from pxr import Gf, UsdGeom


# class for setting the xformable
class UsdObject_helper:
    """
    this class holds the UsdObject and the Xformable object that is attached to the UsdObject
    this will make setting up for loops easyer but you need to remember to delet the class after you are finished

    the class will not automatilcy save the moves you applyed

    Args:
        usd_prim_path (str): the path where the usdObject is located in the usd as a string not as sdf path
    """

    def __init__(self, usd_prim_path, stage):
        # getting the prim from the prim path
        self.usd_prim = stage.GetPrimAtPath(usd_prim_path)

        # setting up the xformable
        self.xformable = UsdGeom.Xformable(self.usd_prim)

    def translate_UsdObject(self, transform: list, movename: str):
        """
        this function will transform an UsdObject with a trasform list and an move name in order to enshure that the
        transform could be muted

        Args:
            transform (list): describes how the object schould be descibed [(t.x,t.y,t.z),(r.x,r.y,r.z),(s.x,s.y,s.z),(uniform_scale)]
            movename (str): every move has / schould have a move in order to mute it if needed this is the name
        """

        # generating the transform matix
        translation_matrix = Gf.Matrix4d().SetTranslate(
            Gf.Vec3d(transform[0][0], transform[0][1], transform[0][2])
        )

        # creating the rotations
        rotation_x = Gf.Rotation(Gf.Vec3d(1.0, 0.0, 0.0), (transform[1][0]))
        rotation_y = Gf.Rotation(Gf.Vec3d(0.0, 1.0, 0.0), (transform[1][1]))
        rotation_z = Gf.Rotation(Gf.Vec3d(0.0, 0.0, 1.0), (transform[1][2]))
        # setting up the rotation matix
        rotation_matrix = Gf.Matrix4d()

        # setting the rotation to the rotation matrix
        rotation_matrix.SetRotate(rotation_x * rotation_y * rotation_z)

        # adding the translation to the rotation matrix in order to get the rotation with the pivot transform from the transform
        rotation_matrix *= translation_matrix

        # creating the scaling matrix
        scaling_matrix = Gf.Matrix4d().SetScale(
            (
                transform[2][0] * transform[3],
                transform[2][1] * transform[3],
                transform[2][2] * transform[3],
            )
        )

        # ading the rotation matrix to the scale matrix to make shure that the scale /
        # is applyed att the pivot location off the transform and the rotation
        # the scaleing matrix is the matrix that contains now transform sclae and rotate
        scaling_matrix *= rotation_matrix

        # setting the created movment matrix as an new mutelbe attribute layer with the movename att as its name
        self.xformable.AddXformOp(UsdGeom.XformOp.TypeTransform, opSuffix=movename).Set(
            value=scaling_matrix
        )

