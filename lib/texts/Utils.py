################################################################################
#
# General Utliities for Blending
#
################################################################################
import bpy


def simplify_curves(error):
    """ Call Simplify f-curves on all selected objects """
    selected = bpy.context.selected_objects.copy()
    old_active = bpy.context.scene.objects.active
    
    for object in selected:
        bpy.context.scene.objects.active = object
        bpy.ops.graph.simplify(error=error)
        
    bpy.context.scene.objects.active = old_active


class SimplifyCurves(bpy.types.Operator):
    """ Simplify f-curves for all selected objects """

    bl_description = "Simplify f-curves for all selected objects"

    bl_idname = 'object.simplify_curves'

    bl_label = 'Simplify f-curves'
    
    @classmethod
    def poll(cls, context):
        """ Blender poll method """
        return True

    def execute(self, context):
        """ Execute utility """
        simplify_curves(0.01)
        return {'FINISHED'}


def clean_unused_objects():
    """ Remove objects with 0 use count from the file """
    groups = [bpy.data.curves, bpy.data.meshes, bpy.data.objects, 
              bpy.data.groups]
    removed = []
    
    for group in groups:
        for object in group:
            if object.users == 0:
                removed.append(object.name)
                group.remove(object, do_unlink=True)
    
    return removed


class CleanUnusedObjects(bpy.types.Operator):
    """ Remove unused objects from the current file. """

    bl_description = "Clean away unused objects"

    bl_idname = 'object.clean_unused_objects'

    bl_label = 'Clean Unused Objects'
    
    @classmethod
    def poll(cls, context):
        """ Blender poll method """
        return True

    def execute(self, context):
        """ Execute utility """
        removed = clean_unused_objects()
        self.report({'INFO'},
                    "removed: %s" % (removed))
        return {'FINISHED'}


class Toolbox(bpy.types.Panel):
    """ Toolbar to provide buttons to invoke utils """

    bl_category = "Toolbox"
    
    bl_context = "objectmode"

    bl_description = "Various Tools"
    
    bl_idname = 'object.toolbox'

    bl_label = 'Toolbox'

    bl_region_type = 'TOOLS'
    
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.clean_unused_objects", text="Clean Unused")
        row = layout.row()
        row.operator("object.simplify_curves",      text="Simplify F-Curves")


def register():
    """ Register Blender Operator """
    bpy.utils.register_class(CleanUnusedObjects)
    bpy.utils.register_class(SimplifyCurves)
    bpy.utils.register_class(Toolbox)


def unregister():
    """ Unregister Blender Operator """
    bpy.utils.unregister_class(Toolbox)
    bpy.utils.unregister_class(SimplifyCurves)
    bpy.utils.unregister_class(CleanUnusedObjects)


if __name__ == '__main__':
    register()
