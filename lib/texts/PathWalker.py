################################################################################
#
# PathWalker
#
# Blender Addon to trace a path object and place objects along the path for
# example a set of dominos
#
################################################################################
import bpy

from bpy.props import (
    EnumProperty,
    FloatVectorProperty,
    FloatProperty,
    IntProperty,
    StringProperty
)
from mathutils import (
    Vector
)

bl_info = \
    {
        'name' :        "PathSimulator",
        'author' :      "Adam Latchem <adamlatchem@gmail.com>",
        'version' :     (1, 0, 0),
        'blender' :     (2, 7, 8),
        'location' :    "View 3D > Object Mode > Tool Shelf",
        'description' : "Place objects with physics along a path",
        'warning' :     "",
        'wiki_url' :    "",
        'tracker_url' : "",
        'category' :    "Add Curve",
    }


def debug_path(operator, frame, location, rotation):
    """ Dump path info to console """
    operator.report({'INFO'},
                    "debug_path: %d %s %s" % (frame, location, rotation))


def draw_domino(frame, location, rotation, dimensions, mass, collision_margin,
                friction, bounciness, group_name, material, simulation_type):
    """ Draw a single domino named for given frame at location with rotation and
        dimensions as supplied. Physics parameters may also be tweaked. """
    location = location + Vector((0, 0, dimensions[2] / 2.0))
    bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
    cube = bpy.context.active_object
    cube.name = "Dominno.%03d" % frame
    bpy.data.groups[group_name].objects.link(cube)
    cube.dimensions = dimensions
    if material:
        cube.data.materials.append(material)

    collision_shape = 'CONVEX_HULL'

    if simulation_type == 'GameEngine':
        physics_object = cube.game
        physics_object.physics_type = 'RIGID_BODY'
        physics_object.use_collision_bounds = True
        physics_object.collision_bounds_type = collision_shape
        physics_object.use_anisotropic_friction = True
        physics_object.friction_coefficients = \
            physics_object.friction_coefficients * friction
    else:
        bpy.ops.rigidbody.object_add()
        physics_object = cube.rigid_body
        physics_object.type = 'ACTIVE'
        physics_object.enabled = True
        physics_object.collision_shape = collision_shape
        physics_object.friction = friction
        physics_object.use_deactivation = True
        physics_object.use_start_deactivated = True
        physics_object.deactivate_linear_velocity = 4.0
        physics_object.deactivate_angular_velocity = 4.0

    physics_object.mass = mass
    physics_object.use_margin = True
    physics_object.collision_margin = collision_margin
    physics_object.restitution = bounciness

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def set_frame(curve, frame):
    """ Set eval_time on curve and update dependent variables """
    curve.data.eval_time = float(frame)
    bpy.context.scene.update()


def walk_curve(operator, curve, steps, walk_function):
    """ Walk curve calling walk_function at each frame """
    if curve is None or not isinstance(curve.data, bpy.types.Curve):
        raise Exception("Select a Curve/Path first")
    curve_data = curve.data
    eval_time = curve_data.eval_time
    active_object = bpy.context.scene.objects.active

    set_frame(curve, 1)
    location = curve.location + curve_data.splines[0].points[0].co.xyz

    empty_object = bpy.data.objects.new(name="Empty", object_data=None)
    empty_object.empty_draw_type = 'ARROWS'
    bpy.context.scene.objects.link(empty_object)

    constraint = empty_object.constraints.new(type='FOLLOW_PATH')
    constraint.target = curve
    curve_data.use_path = True
    animation = curve_data.animation_data_create()
    animation.action = bpy.data.actions.new("%sAction" % curve_data.name)
    f_curve = animation.action.fcurves.new("eval_time")
    modifier = f_curve.modifiers.new('GENERATOR')
    modifier.coefficients = (-1, 1)

    set_frame(curve, 2)
    previous_location = Vector(empty_object.matrix_world.translation)
    set_frame(curve, 1)
    location = empty_object.matrix_world.translation
    direction = location - previous_location
    previous_location = location + direction

    step_to_frame = curve_data.path_duration / float(steps)
    for step in range(1, int(steps) + 1):
        frame = step * step_to_frame
        set_frame(curve, frame)
        direction = location - previous_location
        rot_quat = direction.to_track_quat('X', 'Z')
        rotation = rot_quat.to_euler()
        walk_function(step, location, rotation)
        previous_location = Vector(location)

    bpy.data.objects.remove(empty_object, do_unlink=True)

    bpy.context.scene.objects.active = active_object
    active_object.select = True
    set_frame(curve, eval_time)


class PathWalker(bpy.types.Operator):
    """ Operator walks a path placing new objects along the path as it goes """

    bl_idname = 'object.path_walker'

    bl_label = 'PathWalker'

    bl_options = {'REGISTER', 'UNDO'}

    bl_description = "Path walking tool"

    dimensions = FloatVectorProperty(
        name="dimensions",
        description="Dimensions of a single object",
        default=(0.128, 0.4, 1.120),
        subtype='XYZ'
    )

    material_name = StringProperty(
        name="material name",
        description="Material to assign each object",
        default="",
        subtype='NONE'
    )

    mass = FloatProperty(
        name="mass",
        description="mass of each object",
        default=0.080,
        subtype='NONE',
        unit='NONE'
    )

    collision_margin = FloatProperty(
        name="collision margin",
        description="physics collision margin",
        default=0.001,
        subtype='NONE',
        unit='NONE'
    )

    friction = FloatProperty(
        name="friction",
        description="friction of each object",
        default=0.5,
        subtype='NONE',
        unit='NONE'
    )

    bounciness = FloatProperty(
        name="bounciness",
        description="bounciness of each object",
        default=0.5,
        subtype='NONE',
        unit='NONE'
    )

    number = IntProperty(
        name="number",
        description="The number of objects to place on the path",
        default=5,
        min=1,
        max=10000
    )

    simulation_type = EnumProperty(
        name="simulation type",
        description="Simulation type to use",
        items=['GameEngine', 'RigidBodyPhysics'],
        default='GameEngine'
    )

    @classmethod
    def poll(cls, context):
        """ Blender poll method """
        active_object = context.active_object
        return active_object is not None and active_object.mode == 'OBJECT' and \
            isinstance(active_object.data, bpy.types.Curve)

    def execute(self, context):
        """ Blender operator execute method """
        active_object = context.active_object
        context.object.select = False

        group_name = active_object.name + 'PathWalkerGroup'
        if bpy.data.groups.find(group_name) == -1:
            bpy.data.groups.new(name=group_name)

        material = None
        if len(self.material_name) > 0:
            if bpy.data.materials.find(self.material_name) != -1:
                material = bpy.data.materials[self.material_name]

        def create_domino(frame, location, rotation):
            """ for use with walk_curve to draw a domino """
            #debug_path(self, frame, location, rotation)
            draw_domino(frame, location, rotation,
                        dimensions=self.dimensions, mass=self.mass,
                        collision_margin=self.collision_margin,
                        friction=self.friction, bounciness=self.bounciness,
                        group_name=group_name, material=material,
                        simulation_type=self.simulation_type)

        walk_curve(self, active_object, self.number, create_domino)
        return {'FINISHED'}


def menu_func(self, context):
    """ Add an operator control to a menu """
    self.layout.operator(PathWalker.bl_idname, text='Path Walker',
                         icon='PLUGIN')


def register():
    """ Register Blender Operator """
    bpy.utils.register_class(PathWalker)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    """ Unregister Blender Operator """
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(PathWalker)


if __name__ == '__main__':
    register()
