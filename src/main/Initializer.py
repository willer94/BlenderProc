from src.main.Module import Module
import bpy

def add_shader_on_world():
    bpy.data.worlds['World'].use_nodes = True
    env_node = bpy.data.worlds['World'].node_tree.nodes.new(type='ShaderNodeTexEnvironment')
    back_node = bpy.data.worlds['World'].node_tree.nodes['Background']
    bpy.data.worlds['World'].node_tree.links.new(env_node.outputs['Color'], back_node.inputs['Color'])

class Initializer(Module):
    """ Does some basic initialization of the blender project.

     - Sets background color
     - Configures computing device
     - Creates camera

    **Configuration**:

    .. csv-table::
       :header: "Parameter", "Description"

       "horizon_color", A list of three elements specifying rgb of the world's horizon/background color.
    """

    def __int__(self, config):
        Module.__init__(self, config)

    def run(self):
        # Make sure to use the current GPU 
             
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA'
        bpy.context.scene.frame_end = 0
        print(prefs.compute_device_type, prefs.get_devices())
        for group in prefs.get_devices():
            for d in group:
                d.use = True

        #Set background color
        world = bpy.data.worlds['World']
        world.color[:3] = self.config.get_list("horizon_color", [0.535, 0.633, 0.608])
        world.color[:3] = self.config.get_list("horizon_color", [0., 0., 0.])
        #add_shader_on_world()

        # Create the cam
        cam = bpy.data.cameras.new("Camera")
        cam_ob = bpy.data.objects.new("Camera", cam)
        bpy.context.scene.collection.objects.link(cam_ob)
        bpy.context.scene.camera = cam_ob

        # Use cycles
        bpy.context.scene.render.engine = 'CYCLES'        
