from src.main.Module import Module
import bpy
import numpy as np
from src.utility.Utility import Utility
from add_shader import add_shader_on_ply_object

class ObjLoader(Module):
    """ Just imports the configured .obj file straight into blender

    The import will load all materials into cycle nodes.

    **Configuration**:

    .. csv-table::
       :header: "Parameter", "Description"

       "path", "The path to the .obj file to load."
    """
    def __init__(self, config):
        Module.__init__(self, config)

    def run(self):
        # the default value for forward and axis_up is '-Z' and 'Y'
        # but the rbot model is saved from meshlab, and y axis should be turned
        bpy.ops.import_scene.obj(filepath     = Utility.resolve_path(self.config.get_string("path")),
                                 axis_forward = self.config.get_string("axis_forward", "-Z"),
                                 axis_up      = self.config.get_string("axis_up", "Y") 
                                 )

        for obj in bpy.data.objects:
            if obj.type == 'MESH':                                       
                material = add_shader_on_ply_object(obj)
                nodes = material.node_tree.nodes
                nodes['Diffuse BSDF'].inputs['Roughness'].default_value = np.random.uniform(0.8, 1)
