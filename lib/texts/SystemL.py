################################################################################
#
# Create L systems
#
# systeml_compile generates strings of symbols starting with axiom and applying
# the transformation for each symbol as given in the rules. The process is
# repeated for a given number of iterations.
#
# After generating an lsystem symbol string, the string may be used to call
# functions by 'executing' it. This can be used to drive a simple turtle
# graphics system for example.
#
################################################################################


def systeml_compile_slow(axiom, rules, iterations):
    """ Use rules to replace axiom set number of iterations """
    for iteration in range(0, iterations):
        next_axiom = ""       
        for symbol in axiom:
            if symbol in rules:
                next_axiom = next_axiom + rules[symbol]
            else:
                next_axiom = next_axiom + symbol        
        axiom = next_axiom
            
    return axiom


def systeml_compile(axiom, rules, iterations):
    """ Use rules to replace axiom set number of iterations """
    table = str.maketrans(rules)
    for iteration in range(0, iterations):
        axiom = axiom.translate(table)
    return axiom


def systeml_execute(lsystem, symbol_to_function):
    """ Call functions in symbol_to_function dictionary taking symbols from
        lsystem sequentially """
    for symbol in lsystem:
        symbol_to_function[symbol]()


def systeml_algae(iterations):
    """ A model of the growth of algae """
    return systeml_compile(
        "A",
        {
            "A": "AB",
            "B": "A"
        },
        iterations)


def systeml_pythagoras_tree(iterations):
    """ A pythagorean tree """
    return systeml_compile(
        "0",
        {
            "0": "1[0]0",
            "1": "11"
        },
        iterations)


def systeml_cantor_set(iterations):
    """ The Cantor set """
    return systeml_compile(
        "A",
        {
            "A": "ABA",
            "B": "BBB"
        },
        iterations)


def systeml_koch_curve(iterations):
    """ A Koch curve """
    return systeml_compile(
        "F",
        {
            "F": "F+F-F-F+F"
        },
        iterations)


def systeml_koch_snowflake(iterations):
    """ A beautiful Koch snowflake """
    return systeml_compile(
        "F++F++F",
        {
            "F": "F-F++F-F"
        },
        iterations)


def systeml_sierpinski_triangle(iterations):
    """ The Sierpinski triangle """
    return systeml_compile(
        "F-G-G",
        {
            "F": "F-G+F+G-F",
            "G": "GG"
        },
        iterations)


def systeml_sierpinski_curve(iterations):
    """ A sierpinski curve - approximates the triangle """
    return systeml_compile(
        "A",
        {
            "A": "+B-A-B+",
            "B": "-A+B+A-"
        },
        iterations)


def systeml_dragon_curve(iterations):
    """ The dragon curve """
    return systeml_compile(
        "FX",
        {
            "X": "X+YF+",
            "Y": "-FX-Y"
        },
        iterations)


if __name__ == '__main__':
    import timeit

    n = 100
    t = timeit.timeit(
        "systeml_dragon_curve(15)",
        setup="from __main__ import systeml_dragon_curve",
        number=n)
    print("Single run %.4fs" % (t / n))
