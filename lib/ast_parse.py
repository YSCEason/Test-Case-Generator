import ast
from collections import deque


class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)

    return func_calls

def get_variables(tree):
    variables = []
    func_calls = get_func_calls(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            variables.append(node.id)

    variables = list(set(variables) - set(func_calls))

    return variables

def get_func_calls_info(tree):
    func_calls_info = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)

            # - Args as List - #
            # func_info_list = [callvisitor.name, recursive_get_node_arg(node.args)]

            # - Args as item - #
            func_info_list = [callvisitor.name]
            func_info_list.extend(recursive_get_node_arg(node.args))

            func_calls_info.append(func_info_list)

    return func_calls_info

def recursive_get_node_arg(node_args):
    arg_list = []
    # print node_args
    for node_arg in node_args:
        if isinstance(node_arg, ast.Num):
            # print node_arg
            arg_list.append(node_arg.n)
        elif isinstance(node_arg, ast.List) or isinstance(node_arg, ast.Tuple):
            arg_list.append(recursive_get_node_arg(node_arg.elts))

    return arg_list



def get_expression_variables_list(a_expression):

    expr_parse = ast.parse( a_expression )
    var_list = get_variables( expr_parse )

    return var_list

def get_expression_func_name_list(a_expression):

    expr_parse = ast.parse( a_expression )
    func_list = get_func_calls( expr_parse )

    return func_list

def get_expression_func_info_list(a_expression):

    expr_parse = ast.parse( a_expression )
    func_list = get_func_calls_info( expr_parse )

    return func_list


if __name__ == '__main__':
    reg1 = 10
    reg2 = 20

    eq1 = 'reg1 + 3 + max(100, 200)'
    eq2 = 'reg1 if reg1 > 100 else reg2'
    eq3 = 'reg1 if reg1 > 100 else (reg2 if reg2>200 else 199)'
    eq4 = 'r_sort_desc([0, 19], [0, 255], 10)'


    p1 = ast.parse(eq1)
    p2 = ast.parse(eq2)
    p3 = ast.parse(eq3)
    p4 = ast.parse(eq4)

    print(get_variables(p1))
    print(get_variables(p2))
    print(get_variables(p3))
    print(get_variables(p4))

    print
    print

    print(get_func_calls(p1))
    print(get_func_calls(p2))
    print(get_func_calls(p3))
    print(get_func_calls(p4))
    print
    print

    # print(args(p1))
    print(ast.dump(p4))
    print


    print get_func_calls_info(p4)
    # get_rand_sort_args(p4)
