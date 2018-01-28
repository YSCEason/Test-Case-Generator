import os
import sys
import re
from collections import OrderedDict
import datetime
from execution import CaseEquationExec

class Check_Limitation(object):
    def __init__(self):
        pass

    def check_reg_limitation(self, a_case_idx, a_new_pattern_dict, a_ft_data):

        rtn_result = True
        new_ptn_dict = a_new_pattern_dict
        ft_data      = a_ft_data

        chk_limit_result_dict = OrderedDict()
        for ft_name, sub_ft_data in ft_data.iteritems():
            for reg_name, reg_data in sub_ft_data.iteritems():

                if not sub_ft_data[reg_name]["constraint"] == "__No_Def__":

                    limit_list = sub_ft_data[reg_name]["constraint"]
                    result = self.check_over_limiation(limit_list, new_ptn_dict)

                    chk_limit_result_dict[reg_name] = result

        # pattern gen error report
        for reg_name, reg_result in chk_limit_result_dict.iteritems():
            if not reg_result:
                print ("[Check limitation] func_name: %s, \t Pattern_%05d,  %20s : %s (val=%d)")%(ft_name, a_case_idx, reg_name, reg_result, new_ptn_dict[reg_name])
                rtn_result = False

        return rtn_result

    def check_over_limiation(self, a_limit_list, a_new_ptn_dict):

        for limit_expression in a_limit_list:
            if CaseEquationExec.string_to_limitation(limit_expression, a_new_ptn_dict):
                continue
            else:
                return False
        return True


if __name__ == '__main__':
    pass
