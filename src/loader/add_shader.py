import bpy


def add_shader_on_ply_object(obj):
        
    bpy.ops.material.new()
    material = list(bpy.data.materials)[0]

    material.use_nodes = True
    material.node_tree.links.clear()

    mat_out = material.node_tree.nodes['Material Output']
    diffuse_node = material.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
    gloss_node = material.node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
    attr_node = material.node_tree.nodes.new(type='ShaderNodeAttribute')

    material.node_tree.nodes.remove(diffuse_node)
    attr_node.attribute_name = 'Col'
    material.node_tree.links.new(attr_node.outputs['Color'], gloss_node.inputs['Color'])
    material.node_tree.links.new(gloss_node.outputs['BSDF'], mat_out.inputs['Surface'])

    obj.data.materials.append(material)
    return material