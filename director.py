#!/Blender --python
#
# Apply common configurations and initiate procedures in blend files
#
import bpy
import sys

def bake_ocean():
    """ Bake ocean in selected scene """
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    scene = argv[0]

    the_scene = bpy.data.scenes[scene]
    bpy.context.window.scene = the_scene
    for obj in the_scene.objects:
        for modifier in obj.modifiers:
            if modifier.type == 'OCEAN':
                print(f'Baking ocean {the_scene.name} > {obj.name}.{modifier.name}')
                bpy.ops.object.ocean_bake(modifier=modifier.name, free=False)
                print("Done.")
                break
    exit(0)

bake_ocean()

