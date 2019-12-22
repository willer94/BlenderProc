from src.main.Module import Module
import bpy
import mathutils
import os
from math import radians
import numpy as np
from .add_shader import add_shader_on_ply_object
from src.utility.Utility import Utility

class PlyLoader(Module):

    def __init__(self, config):
        Module.__init__(self, config)

    def run(self):
        """Just imports the configured .ply file straight into blender

        """
        if not self.config.get_bool('is_replica_object', False):

            bpy.ops.import_mesh.ply(filepath = Utility.resolve_path(self.config.get_string("path")))
        else:
            file_path = os.path.join(self.config.get_string('data_path'), self.config.get_string('data_set_name'), 'mesh.ply')
            if os.path.exists(file_path):
                bpy.ops.import_mesh.ply(filepath=file_path)
            else:
                raise Exception("The filepath is not known: {}".format(file_path))
        if self.config.get_bool('use_ambient_occlusion', False):
            bpy.context.scene.world.light_settings.use_ambient_occlusion = True  # turn AO on
            bpy.context.scene.world.light_settings.ao_factor = 0.9  # set it to 0.5
        if self.config.get_bool('use_smooth_shading', False):
            for poly in bpy.data.objects['mesh'].data.polygons:
                poly.use_smooth = True

        # for obj in bpy.data.objects:
        #     if obj.type == 'MESH':                                       
        #         material = add_shader_on_ply_object(obj)
        #         nodes = material.node_tree.nodes
        #         nodes['Glossy BSDF'].inputs['Roughness'].default_value = np.random.uniform(0.8, 1)

        cur_obj = bpy.context.selected_objects[-1]
        #mat = cur_obj.data.materials.get("Material")
        #if mat is None:
        mat = self.add_shader_on_ply_object(cur_obj)
        #mat = self._load_materials
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