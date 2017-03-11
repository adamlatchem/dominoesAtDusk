################################################################################
#
# Helper to render some LSystems with CrushGraphics
#
################################################################################
import CrushGraphics
import SystemL


def render_dragon():
    dragon = SystemL.systeml_dragon_curve(5)
    
    turtle = CrushGraphics.Crush()
    turtle.pen_down()
    
    SystemL.systeml_execute(dragon,
    {
        "F": lambda : turtle.forward(2),
        "+": lambda : turtle.turn( CrushGraphics.PI_BY_TWO),
        "-": lambda : turtle.turn(-CrushGraphics.PI_BY_TWO),
        "X": lambda : None,
        "Y": lambda : None,
    })


def render_koch_snowflake():
    iterations = 4
    snowflake = SystemL.systeml_koch_snowflake(iterations)
    
    turtle = CrushGraphics.Crush()
    turtle.pen_down()
    
    SystemL.systeml_execute(snowflake,
    {
        "F": lambda : turtle.forward(1.0 / pow(3, iterations)),
        "+": lambda : turtle.turn( CrushGraphics.PI_BY_THREE),
        "-": lambda : turtle.turn(-CrushGraphics.PI_BY_THREE)
    })
    
    
if __name__ == '__main__':
    render_koch_snowflake()
