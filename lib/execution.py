import random
import ast
from pprint import pprint
import exec_subfunc

_support_dict = {"__builtins__": None,       # return int
                                             'i_max'                 :  exec_subfunc._max,
                                             'i_min'                 :  exec_subfunc._min,
                                             'i_randint'             :  exec_subfunc._randint,
                                             'i_randlist'            :  exec_subfunc._randlist,
                                             'i_rand_align'          :  exec_subfunc._rand_align,
                                             'i_rand_even'           :  exec_subfunc._rand_even,
                                             'i_rand_odd'            :  exec_subfunc._rand_odd,
                                             'i_max_bits'            :  exec_subfunc._max_bits,
                                             'i_align_ceil'          :  exec_subfunc._align_ceil,
                                             'i_align_floor'         :  exec_subfunc._align_floor,

                                             # return list[]
                                             'lut_sort_incre'        :  exec_subfunc._lut_sort_incre,
                                             'lut_sort_desc'         :  exec_subfunc._lut_sort_desc,
                                             'lut_sort_incre_align'  :  exec_subfunc._lut_sort_incre_align,
                                             'lut_sort_desc_align'   :  exec_subfunc._lut_sort_desc_align,
                                             'lut_rand'              :  exec_subfunc._lut_rand,
                                             'lut_rand_align'        :  exec_subfunc._lut_rand_align
                }


_support_limit_dict = {"__builtins__": None, # return bool
                                             'chk_align'             :  exec_subfunc._check_align,
                                             'chk_even'              :  exec_subfunc._check_even,
                                             'chk_odd'               :  exec_subfunc._check_odd
                      }


class CaseEquationExec:

    @staticmethod
    def string_to_execution(expression, data_dict):

        exec(expression, _support_dict, data_dict)
        return data_dict

    @staticmethod
    def string_to_assignment(expression, data_dict):
        # return eval(expression, {"__builtins__": None}, data_dict)
        return eval(expression, _support_dict, data_dict)

    @staticmethod
    def string_to_limitation(expression, data_dict):
        return eval(expression, _support_limit_dict, data_dict)



if __name__ == '__main__':

    # expression = "r_if_else( 'rg_in_width>20', '3', '2')"
    # expression = " 3 if (rg_in_width>20) else 2"
    expression = ("( r_randint(reg2, reg3) ) if ( rg_in_width>20 ) else ( (22) if(reg3>4) else(5) )")

    # data_dict = { "rg_in_width" : 30,
    #               "reg2" : 20,
    #               "reg3" : 40
    #             }
    # result = CaseEquationExec.string_to_assignment(expression, data_dict)
    # print result

    # ex = ast.parse(expression, mode = 'eval')
    # print ex
    # pprint(ast.dump(ex))


