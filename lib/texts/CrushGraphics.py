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

from math import pi as PI
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
    res = {}                                                               
    count = 0
    for area in bpy.context.screen.areas:                                  
        res[area.type] = count                                             
        count = count + 1
    return res  


class Squirt(object):
    """ State for Crush """
    
    pen_down = False
    
    rotation = 0
    
    location = Vector()
    
    def direction(self):
        """ Return the current direction vector """
        direction = Vector((1,0,0))
        rotation = Quaternion((0,0,1), self.rotation)
        direction.rotate(rotation)
        return direction
    
    def forward(self, distance):
        """ Move forward the given distance """
        self.location = self.location + distance * self.direction()
    
    def turn(self, angle):
        """ Rotate by given number of radians and normalise to +/-PI """
        self.rotation = self.rotation + angle
        while self.rotation > PI:
            self.rotation = self.rotation - TWO_PI
        while self.rotation < -PI:
            self.rotation = self.rotation + TWO_PI


class Crush(object):
    """ A turtle grpahics like object for paths in Blender """
    
    state = [Squirt()]
    
    def __init__(self):
        """ Initially place ourselves at the 3D cursor """
        areas = areas_tuple()
        view3d = bpy.context.screen.areas[areas['VIEW_3D']].spaces[0]
        self.state[-1].location = \
            copy.copy(view3d.cursor_location)
        
    def pen_up(self):
        """ Raise the pen """
        self.state[-1].pen_down = False
        
    def pen_down(self):
        """ Lower the pen """
        self.state[-1].pen_down = True

    def forward(self, distance):
        """ Move crush forward the given distance in current direction leaving
            a trail if the pen is down """
        state = self.state[-1]
        
        if state.pen_down:
            start = copy.copy(state.location)
        
        state.forward(distance)

        if state.pen_down:
            radius = distance / 2.0
            mid_point = start + radius * state.direction()
            rotation = (0, 0, state.rotation)
            path = bpy.ops.curve.primitive_nurbs_path_add(
                location=mid_point, radius=radius / 2.0, rotation=rotation)
            bpy.ops.object.transform_apply(location=False,
                rotation=True, scale=True)

    def push(self):
        """ push state onto stack """
        self.state.append(copy.copy(state[-1]))
        
    def pop(self):
        """ pop state from stack """
        self.state.pop()        
        
    def turn(self, angle):
        """ Rotate by given number of radians """
        self.state[-1].turn(angle)


def example():
    crush = Crush()
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
