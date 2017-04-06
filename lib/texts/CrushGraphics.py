################################################################################
#
# Turtle Paths
#
# Create paths in blender using similar primitives to those found in turtle
# graphics systems such as Logo.
#
# Crush is the turtle from finding nemo,. Squirt, his son, helps him on his
# journey ...
#
################################################################################
import bpy
import copy

from math import (
    pi as PI,
    floor
)
from mathutils import (
    Vector,
    Quaternion
)


# 360 degrees
TWO_PI = 2.0 * PI

# 90 degrees
PI_BY_TWO = PI / 2.0

# 60 degrees
PI_BY_THREE = PI / 3.0


def areas_tuple():
    """ Get map of screen area to index in list """
    res = {}
    count = 0
    for area in bpy.context.screen.areas:
        res[area.type] = count
        count = count + 1
    return res


def verts_to_points(verts, spline_type):
    """
    Adapted from blenders curave_aceous module.
    """
    # main vars
    vert_array = []

    # array for BEZIER spline output (V3)
    if spline_type == 'BEZIER':
        for v in verts:
            vert_array += v

    # array for nonBEZIER output (V4)
    else:
        for v in verts:
            vert_array += v
            if spline_type == 'NURBS':
                vert_array.append(1)  # for nurbs w=1
            else:  # for poly w=0
                vert_array.append(0)
    return vert_array


def setBezierHandles(obj, mode):
    """
    Adapted from blenders curave_aceous module.
    """
    scene = bpy.context.scene
    if obj.type != 'CURVE':
        return
    scene.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT', toggle=True)
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.handle_type_set(type=mode)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=True)


def create_curve(context, name, vert_array, self, align_matrix):
    """
    Create new CurveObject from vertarray and splineType.

    Adapted from blenders curve_aceous module.
    """
    # options to vars
    spline_type = self.spline_type

    # create curve
    scene = context.scene
    new_curve = bpy.data.curves.new(name + '-curve', type='CURVE')
    new_spline = new_curve.splines.new(type=spline_type)  # spline

    # create spline from vertarray
    if spline_type == 'BEZIER':
        new_spline.bezier_points.add(int(len(vert_array)*0.33))
        new_spline.bezier_points.foreach_set('co', vert_array)
    else:
        new_spline.points.add(int(len(vert_array)*0.25 - 1))
        new_spline.points.foreach_set('co', vert_array)

    # set curveOptions
    new_curve.dimensions = '2D'
    new_curve.use_path = self.use_path
    new_spline.use_cyclic_u = self.use_cyclic_u
    new_spline.use_endpoint_u = self.endp_u
    new_spline.order_u = self.order_u

    # create object with newCurve
    new_obj = bpy.data.objects.new(name + '-object', new_curve)
    scene.objects.link(new_obj)  # place in active scene
    new_obj.select = True  # set as selected
    scene.objects.active = new_obj  # set as active
    if align_matrix:
        new_obj.matrix_world = align_matrix  # apply matrix

    # set bezierhandles
    if spline_type == 'BEZIER':
        setBezierHandles(new_obj, self.handle_type)

    return new_obj


class Squirt(object):
    """ State for Crush """

    def __init__(self):
        """ Ctor """
        self.pen_down = False
        self.rotation = 0
        self.location = Vector()
        self.path = [[0, 0, 0]]
        self.spline_type = None

    def new_path(self):
        """ Sart a new path """
        self.path = []
        self.extend_path()

    def extend_path(self):
        """ Append current location to the path """
        location = self.location
        self.path.append([location.x, location.y, location.z])

    def direction(self):
        """ Return the current direction vector """
        direction = Vector((1, 0, 0))
        rotation = Quaternion((0, 0, 1), self.rotation)
        direction.rotate(rotation)
        return direction

    def forward(self, distance):
        """ Move forward the given distance """
        self.location = self.location + distance * self.direction()
        self.extend_path()

    def turn(self, angle):
        """ Rotate by given number of radians and normalise to +/-PI """
        if self.spline_type == 'NURBS':
            # So the spline subdivisions don't cut corners
            self.extend_path() 
        self.rotation = self.rotation + angle        
        self.rotation = self.rotation - \
            TWO_PI * floor((self.rotation + PI) / TWO_PI)


class Crush(object):
    """ A turtle graphics like object for paths in Blender. A path history
        is constructed and rendered as a single curve when pen_up() is
        invoked. """

    def __init__(self, group_name, spline_type):
        """ Initially place ourselves at the 3D cursor """
        # Curve is closed
        self.use_cyclic_u = False
        # Stretch to endpoints
        self.endp_u = True
        # Order of the NURBS spline
        self.order_u = 2
        # Use curve as animation path
        self.use_path = True
        # For Bezier curve
        self.handle_type = 'AUTOMATIC'
        self.group = bpy.data.groups.new(group_name)
        # 'POLY', 'NURBS' or 'BEZIER'
        self.spline_type = spline_type
        areas = areas_tuple()
        view3d = bpy.context.screen.areas[areas['VIEW_3D']].spaces[0]
        self.state = [Squirt()]
        self.state[-1].spline_type = self.spline_type
        self.state[-1].location = \
            copy.copy(view3d.cursor_location)

    def pen_up(self):
        """ Raise the pen """
        state = self.state[-1]
        state.pen_down = False
        if len(state.path) > 1:
            self.create_path()

    def pen_down(self):
        """ Lower the pen """
        self.state[-1].pen_down = True

    def forward(self, distance):
        """ Move crush forward the given distance in current direction leaving
            a trail if the pen is down """
        self.state[-1].forward(distance)

    def push(self):
        """ push state onto stack """
        state_copy = copy.copy(self.state[-1])
        self.state.append(state_copy)

    def pop(self):
        """ pop state from stack """
        self.state.pop()

    def turn(self, angle):
        """ Rotate by given number of radians """
        self.state[-1].turn(angle)

    def create_path(self):
        """ Take current state and render its path as a curve """
        state = self.state[-1]
        vertex_array = verts_to_points(state.path, self.spline_type)
        curve = create_curve(bpy.context, self.group.name,
            vertex_array, self, None)
        self.group.objects.link(curve)
        state.new_path()


def test():
    """ Used to test during development """
    crush = Crush("I_am_square", 'BEZIER')
    right_90 = -PI_BY_TWO
    crush.pen_down()
    crush.forward(1)
    crush.turn(right_90)
    crush.forward(1)
    crush.turn(right_90)
    crush.forward(1)
    crush.turn(right_90)
    crush.forward(1)
    crush.turn(right_90)
    crush.pen_up()


if __name__ == '__main__':
    test()