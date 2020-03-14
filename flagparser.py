# A cool flag parser
# Author: Codian

import ast

def _get_datatype(s):
    try:
        return type(ast.literal_eval(s))
    except:
        return str

class Argument:
    def __init__(self, name, data_type, optional=False):
        self.data_type = data_type
        self.optional = optional
        self.name = name

    def get_syntax(self, with_type=False):
        out = self.name

        if with_type:
            if self.data_type == int:
                out = '(Number) '+out
            elif self.data_type == float:
                out = '(Decimal) '+out
            elif self.data_type == str:
                out = '(Text) '+out
            elif self.data_type == bool:
                out = '(State) '+out
        if self.optional:
            return f'[{out}]'
        return f'<{out}>'

class Flag:
    def __init__(self, name: str):
        self.name = name
        self.args = []

    def add_arg(self, name, data_type, optional=False):
        if len(self.args) > 0 and self.args[-1].optional and not optional:
            raise AttributeError(f'required argument follows an optional one ({self.args[-1].name} is optional)')

        self.args.append(
            Argument(name, data_type, optional)
        )

    def get_syntax(self, with_types=False):
        if len(self.args) < 1:
            return self.name
        return self.name + ' ' + '  '.join([i.get_syntax(with_types) for i in self.args])

class ParsingError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = 'Unknown Error while parsing flags.'
        super().__init__(message)

class UnexpectedArgument(ParsingError):
    def __init__(self, arg):
        message = f'Encountered unexpected argument "{arg}"'
        super().__init__(message)

class MissingRequiredArgument(ParsingError):
    def __init__(self, flag, arg):
        message = f'Flag "{flag}" is missing required argument "{arg}"'
        super().__init__(message)

class InvalidArgument(ParsingError):
    def __init__(self, flag, arg, value):
        got = _get_datatype(value)
        expected = arg.data_type
        message = f'Invalid argument "{arg.name}" (of flag "{flag}"), got {got} (value={value}), expected {expected}'
        super().__init__(message)

class Parser:
    def __init__(self):
        self.flags = {}

    def add_flag(self, flag):
        self.flags[flag.name] = flag

    def _compare_datatypes(self, a, b, strict_int=True, strict_float=False):
        if a == int and b == float and not strict_float:
            return True
        elif a == float and b == int and not strict_int:
            return True
        elif a == b:
            return True
        elif b == str and (a == float or a == int):
            return True
        return False

    def parse(self, inparray, allow_stray_args=True):
        unfulfilled_optional = []
        unfulfilled_required = []

        flag = None

        mapping = {}

        for element in inparray:
            if len(unfulfilled_required) > 0:
                if self._compare_datatypes(
                        _get_datatype(element),
                        unfulfilled_required[0].data_type
                ):
                    mapping[flag][unfulfilled_required[0]] = element
                    del unfulfilled_required[0]
                else:
                    raise InvalidArgument(
                        flag.name,
                        unfulfilled_required[0],
                        element
                    )

            elif len(unfulfilled_optional) > 0:
                if self._compare_datatypes(
                        _get_datatype(element),
                        unfulfilled_optional[0].data_type
                ):
                    mapping[flag][unfulfilled_optional[0]] = element
                    del unfulfilled_optional[0]
                else:
                    raise InvalidArgument(
                        flag.name,
                        element,
                        _get_datatype(element),
                        unfulfilled_optional[0].data_type
                    )

            elif element in self.flags.keys():
                flag = self.flags[element]

                unfulfilled_optional = [i for i in flag.args if i.optional]
                unfulfilled_required = [i for i in flag.args if not i.optional]

                mapping[flag] = {}
            else:
                if not allow_stray_args and flag is not None:
                    raise UnexpectedArgument(element)
                mapping[Argument(element, _get_datatype(element))] = None

        if len(unfulfilled_required):
            raise MissingRequiredArgument(flag.name, unfulfilled_required[0].name)
        return mapping

if __name__ == '__main__':
    print('This file does nothing.')
    print('It is intended to be used as a dependency for other programs.')
    input('[press enter to exit] ')
