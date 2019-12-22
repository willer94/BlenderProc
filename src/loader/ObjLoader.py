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

        cur_obj = bpy.context.selected_objects[-1]

        mat = cur_obj.data.materials.get("Material")
        if mat is None:
            # mat = self.add_shader_on_ply_object(cur_obj)
            mat = self._load_materials
            self._link_col_node(mat)    

    def add_shader_on_ply_object(self, obj):
        bpy.ops.material.new()
        material = list(bpy.data.materials)[0]

        material.use_nodes = True
        material.node_tree.links.clear()

        mat_out = material.node_tree.nodes['Material Output']        
        attr_node = material.node_tree.nodes.new(type='ShaderNodeAttribute')        
        attr_node.attribute_name = 'Col'        
        material.node_tree.links.new(attr_node.outputs['Color'], mat_out.inputs['Surface'])

        obj.data.materials.append(material)        

        return material

    def _load_materials(self, cur_obj):
        """ Loads / defines materials, e.g. vertex colors 
        
        :param object: The object to use.
        """

        mat = cur_obj.data.materials.get("Material")
        
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="Material")

        mat.use_nodes = True

        if cur_obj.data.materials:
            # assign to 1st material slot
            cur_obj.data.materials[0] = mat
        else:
            # no slots
            cur_obj.data.materials.append(mat)

        # if cur_obj.data.vertex_colors:
        #     color_layer = cur_obj.data.vertex_colors["Col"]
        return mat

    def _link_col_node(self, mat):
        """Links a color attribute node to a Principled BSDF node 

        :param object: The material to use.
        """
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        attr_node = nodes.new(type='ShaderNodeAttribute')
        attr_node.attribute_name = 'Col'

        principled_node = nodes.get("Principled BSDF")

        links.new(attr_node.outputs['Color'], principled_node.inputs[0])