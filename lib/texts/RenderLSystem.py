import CrushGraphics
import SystemL

if __name__ == '__main__':
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