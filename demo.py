# Demo of the flag parser

from flagparser import Flag, Argument, Parser

# create a flag object
f1 = Flag('-flip')

# you can also add arguments to the flag object
f2 = Flag('-skew')
f2.add_arg('x', int)
f2.add_arg('y', int)

# you can specify the argument's datatype (float, int, str, bool)
f3 = Flag('-inflate')
f3.add_arg('amount', float)

# add optional arguments to a flag
f4 = Flag('-clean')
f4.add_arg('amount', int, optional=True)

# example flag
f5 = Flag('-addtext')
f5.add_arg('x', int)
f5.add_arg('y', int)
f5.add_arg('text', str)
f5.add_arg('color', str)

# create parser class
parser = Parser()

# add all the flags
parser.add_flag(f1)
parser.add_flag(f2)
parser.add_flag(f3)
parser.add_flag(f4)
parser.add_flag(f5)

# input has to be sanitized beforehand, args should be separated into a list to feed into the parser
test_input = ['-flip', '-skew', '120', '0', '-inflate', '10.5', '-addtext', '0', '200', 'a', '-clean', '20']

# feed the parser your data
mapping = parser.parse(test_input)

# just a way to visualise it, this is not required
for k, v in mapping.items():
    if isinstance(k, Flag):
        print(f'Flag: {k.name}')
        if len(v.keys()) > 0:
            for a, av in v.items():
                print(f'    {a.name} = {av}')
        else:
            print('    (no args)')
    else:
        print(f'Argument: {k.name}')
