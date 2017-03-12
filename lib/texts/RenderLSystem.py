################################################################################
#
# Helper to render some LSystems with CrushGraphics
#
################################################################################
import CrushGraphics
import SystemL


def render_dragon():
    """ Render the dragon l-system """
    dragon_renderer = {
        "F": lambda: turtle.forward(2),
        "+": lambda: turtle.turn(CrushGraphics.PI_BY_TWO),
        "-": lambda: turtle.turn(-CrushGraphics.PI_BY_TWO),
        "X": lambda: None,
        "Y": lambda: None,
    }

    dragon = SystemL.systeml_dragon_curve(5)

    turtle = CrushGraphics.Crush("DragonCurve")
    turtle.pen_down()
    SystemL.systeml_execute(dragon, dragon_renderer)
    turtle.pen_up()


def render_koch_snowflake():
    """ render a Koch snowflake curve """
    snowflake_renderer = {
        "F": lambda: turtle.forward(1.0 / pow(3, iterations)),
        "+": lambda: turtle.turn(CrushGraphics.PI_BY_THREE),
        "-": lambda: turtle.turn(-CrushGraphics.PI_BY_THREE)
    }

    for iterations in range(0, 5):
        snowflake = SystemL.systeml_koch_snowflake(iterations)

        turtle = CrushGraphics.Crush("KochSnowflake-%d" % iterations)
        turtle.pen_down()
        SystemL.systeml_execute(snowflake, snowflake_renderer)
        turtle.pen_up()


if __name__ == '__main__':
    render_koch_snowflake()
