import os
import sys
import re
import random
from collections import OrderedDict
import datetime
from execution import CaseEquationExec
import ast_parse
import ast


class PtnGen_Manage(object):
    def __init__(self):

        self.reg_data_dict = OrderedDict()
        self.reg_flag_dict = OrderedDict()

    # ======================== [Pattern gen] attribute selection ========================

    def get_random_dict(self, a_ini_data, a_sub_ft_info):

        ini_data    = a_ini_data
        sub_ft_info = a_sub_ft_info

        rtn_dict = OrderedDict()

        # 0. reset data and flag dict
        self.reset_func_data_and_flag_dict( sub_ft_info, ini_data )
        reg_data_dict  = self.reg_data_dict
        reg_flag_dict = self.reg_flag_dict



        # 1: independent method
        for reg_name, reg_info in sub_ft_info.iteritems():

            # Check the "ind_method" attribute is exist
            if not (reg_info["ind_method"] == "__No_Def__"):
                reg_data_dict[reg_name]  = CaseEquationExec.string_to_assignment(reg_info["ind_method"], reg_data_dict)
                reg_flag_dict[reg_name] = True

            # if all attribute is not exist, then assign random(min, max)
            elif reg_info["corr_method"] == "__No_Def__":

                min_temp = self.get_min_dict(ini_data, sub_ft_info)
                max_temp = self.get_max_dict(ini_data, sub_ft_info)

                reg_data_dict[reg_name]  = random.randint(min_temp[reg_name], max_temp[reg_name])
                reg_flag_dict[reg_name] = True


        # 2. corresponding method
        is_corr_method_pass = self.update_corr_method_dict( "corr_method", sub_ft_info, reg_flag_dict, reg_data_dict )
        if not is_corr_method_pass:
            print "[__ERROR__] corresponding method failed"


        rtn_dict = reg_data_dict
        return rtn_dict

    def get_constant_dict(self, a_ini_data, a_sub_ft_info):

        ini_data    = a_ini_data
        sub_ft_info = a_sub_ft_info

        rtn_dict = OrderedDict()

        # 0. reset data and flag dict
        self.reset_func_data_and_flag_dict( sub_ft_info, ini_data )
        reg_data_dict = self.reg_data_dict
        reg_flag_dict = self.reg_flag_dict


        # 2. corresponding method
        is_corr_method_pass = self.update_corr_method_dict( "constant", sub_ft_info, reg_flag_dict, reg_data_dict )
        if not is_corr_method_pass:
            print "[__ERROR__] attr:'constant', corresponding method failed"


        rtn_dict = reg_data_dict
        return rtn_dict

    def get_min_dict(self, a_ini_data, a_sub_ft_info):

        ini_data    = a_ini_data
        sub_ft_info = a_sub_ft_info

        rtn_dict = OrderedDict()

        # 0. reset data and flag dict
        self.reset_func_data_and_flag_dict( sub_ft_info, ini_data )
        reg_data_dict  = self.reg_data_dict
        reg_flag_dict = self.reg_flag_dict

        # 2. corresponding method
        is_corr_method_pass = self.update_corr_method_dict( "min", sub_ft_info, reg_flag_dict, reg_data_dict )
        if not is_corr_method_pass:
            print "[__ERROR__] attr:'min', corresponding method failed"


        rtn_dict = reg_data_dict
        return rtn_dict

    def get_max_dict(self, a_ini_data, a_sub_ft_info):

        ini_data    = a_ini_data
        sub_ft_info = a_sub_ft_info

        rtn_dict = OrderedDict()

        # 0. reset data and flag dict
        self.reset_func_data_and_flag_dict( sub_ft_info, ini_data )
        reg_data_dict  = self.reg_data_dict
        reg_flag_dict = self.reg_flag_dict


        # 2. corresponding method
        is_corr_method_pass = self.update_corr_method_dict( "max", sub_ft_info, reg_flag_dict, reg_data_dict )
        if not is_corr_method_pass:
            print "[__ERROR__] attr:'max', corresponding method failed"


        rtn_dict = reg_data_dict
        return rtn_dict

    def get_default_dict(self, a_ini_data, a_sub_ft_info):

        ini_data    = a_ini_data
        sub_ft_info = a_sub_ft_info

        rtn_dict = OrderedDict()

        # 0. reset data and flag dict
        self.reset_func_data_and_flag_dict( sub_ft_info, ini_data )
        reg_data_dict  = self.reg_data_dict
        # reg_flag_dict = self.reg_flag_dict

        rtn_dict = reg_data_dict
        return rtn_dict

    def get_ptnlist_dict(self, a_ini_data, a_sub_ft_info, a_ft_ptn_cnt):

        ini_data    = a_ini_data
        sub_ft_info = a_sub_ft_info
        ft_ptn_cnt  = a_ft_ptn_cnt

        rtn_dict = OrderedDict()

        # 0. reset data and flag dict
        self.reset_func_data_and_flag_dict( sub_ft_info, ini_data )
        reg_data_dict = self.reg_data_dict
        reg_flag_dict = self.reg_flag_dict


        # 1: independent method
        for reg_name, reg_info in sub_ft_info.iteritems():
            if (reg_info["ptnlist"] == "__No_Def__"):
                reg_flag_dict[reg_name] = True


        # 2. corresponding method
        is_corr_method_pass = self.update_list_corr_method_dict( "ptnlist", sub_ft_info, reg_flag_dict, reg_data_dict, ft_ptn_cnt )
        if not is_corr_method_pass:
            print "[__ERROR__] attr:'min', corresponding method failed"


        rtn_dict = reg_data_dict
        return rtn_dict



    # ======================== [Pattern gen] common function ========================

    def reset_func_data_and_flag_dict(self, a_sub_ft_info, a_ini_data):

        # initial the data and flag dict for sub function
        self.reg_data_dict  = OrderedDict()
        self.reg_flag_dict = OrderedDict()

        for reg_name, reg_info in a_sub_ft_info.iteritems():
            self.reg_data_dict[reg_name]  = a_ini_data[reg_name]
            self.reg_flag_dict[reg_name] = False
        pass

    def update_corr_method_dict(self, a_reg_attr, a_sub_ft_info, a_reg_flag_dict, a_reg_data_dict):

        rtn_val = True

        reg_attribute = a_reg_attr
        reg_flag_dict = a_reg_flag_dict
        sub_ft_info   = a_sub_ft_info
        reg_data_dict = a_reg_data_dict

        flag_ok_count = 0
        attempts_cnt  = 0
        max_attempts  = 50
        while ( flag_ok_count != len(reg_flag_dict) ):
            flag_ok_count = 0

            for reg_name, reg_info in sub_ft_info.iteritems():

                # Check the "corr_method" attribute is exist
                if not (reg_info[reg_attribute] == "__No_Def__"):

                    if (not reg_flag_dict[reg_name]) and (reg_info["keyword"] != "__No_Def__"):
                        # Check if the expression is lut
                        lut_data = CaseEquationExec.string_to_assignment(reg_info[reg_attribute], reg_data_dict)
                        self.update_lut_data(reg_info["keyword"], reg_info["LutIdxRange"], reg_flag_dict, reg_data_dict, lut_data)

                    if not (reg_flag_dict[reg_name]):
                        # Check if the expression is corresponding
                        corr_flag = self.check_expre_contain_corr_var(reg_info[reg_attribute], reg_flag_dict)
                        if (corr_flag == 0):
                            reg_data_dict[reg_name] = CaseEquationExec.string_to_assignment(reg_info[reg_attribute], reg_data_dict)
                            reg_flag_dict[reg_name] = True

                if (reg_flag_dict[reg_name]):
                    flag_ok_count += 1

            attempts_cnt += 1
            if (attempts_cnt > max_attempts):
                rtn_val = False
                break

        return rtn_val

    def update_list_corr_method_dict(self, a_reg_attr, a_sub_ft_info, a_reg_flag_dict, a_reg_data_dict, a_ft_ptn_cnt):

        rtn_val = True

        reg_attribute = a_reg_attr
        reg_flag_dict = a_reg_flag_dict
        sub_ft_info   = a_sub_ft_info
        reg_data_dict = a_reg_data_dict


        flag_ok_count = 0
        attempts_cnt  = 0
        max_attempts  = 50
        while ( flag_ok_count != len(reg_flag_dict) ):
            flag_ok_count = 0

            for reg_name, reg_info in sub_ft_info.iteritems():

                if (a_ft_ptn_cnt >= len(reg_info[a_reg_attr])):
                    ft_ptn_cnt = len(reg_info[a_reg_attr]) - 1
                else:
                    ft_ptn_cnt = a_ft_ptn_cnt

                # Check the "corr_method" attribute is exist
                if not (reg_info[reg_attribute] == "__No_Def__"):

                    if (not reg_flag_dict[reg_name]) and (reg_info["keyword"] != "__No_Def__"):
                        # Check if the expression is lut
                        lut_data = CaseEquationExec.string_to_assignment(reg_info[reg_attribute][ft_ptn_cnt], reg_data_dict)
                        self.update_lut_data(reg_info["keyword"], reg_info["LutIdxRange"], reg_flag_dict, reg_data_dict, lut_data)

                    if not (reg_flag_dict[reg_name]):
                        # Check if the expression is corresponding
                        corr_flag = self.check_expre_contain_corr_var(reg_info[reg_attribute][ft_ptn_cnt], reg_flag_dict)
                        if (corr_flag == 0):
                            reg_data_dict[reg_name] = CaseEquationExec.string_to_assignment(reg_info[reg_attribute][ft_ptn_cnt], reg_data_dict)
                            reg_flag_dict[reg_name] = True


                if (reg_flag_dict[reg_name]):
                    flag_ok_count += 1

            attempts_cnt += 1
            if (attempts_cnt > max_attempts):
                rtn_val = False
                break

        return rtn_val

    def check_expre_contain_corr_var(self, a_expression, a_flag_dict):
        # Check the expression contains corresponding variables
        # rtn_flag : False -> independent
        #            True  -> corresponding

        rtn_flag = False

        var_list = ast_parse.get_expression_variables_list(a_expression)

        for reg_key in var_list:
            if( not a_flag_dict[reg_key] ):
                rtn_flag = True
                break

        return rtn_flag

    def update_lut_data(self, a_key_word, a_lut_range, a_reg_flag_dict, a_reg_data_dict, a_lut_data):

        lut_data      = a_lut_data
        reg_data_dict  = a_reg_data_dict
        reg_flag_dict = a_reg_flag_dict
        lut_range     = a_lut_range

        for ii in range(lut_range[0], lut_range[1]+1):
            reg_name = a_key_word.replace("[Idx]", str(ii))

            if(type(lut_data) is list):
                reg_data_dict[reg_name]  = lut_data[ii]
            else:
                reg_data_dict[reg_name]  = lut_data

            reg_flag_dict[reg_name] = True




    # ======================== [Pattern gen] main entry      ========================

    def get_pattern_dict(self, a_ptn_cond_dict, a_ft_ptn_cnt, a_ini_data, a_ft_data, a_rand_seed):

        # {user_define, random, constant, min, max, default}

        random.seed(a_rand_seed)

        ptn_cond = a_ptn_cond_dict

        ft_data  = a_ft_data
        ini_data = a_ini_data

        sub_ft_dict = OrderedDict()
        rtn_data_dict = OrderedDict()

        # loop all funcDef for one pattern
        for ft_name, sub_ft_data in ft_data.iteritems():

            # print "\n\n" + ">>>>>>>>>" + ft_name + "<<<<<<<<" + ptn_cond[ft_name]
            if(ptn_cond[ft_name] == "random"):
                sub_ft_dict = self.get_random_dict(ini_data, sub_ft_data)
            elif(ptn_cond[ft_name] == "constant"):
                sub_ft_dict = self.get_constant_dict(ini_data, sub_ft_data)
            elif(ptn_cond[ft_name] == "min"):
                sub_ft_dict = self.get_min_dict(ini_data, sub_ft_data)
            elif(ptn_cond[ft_name] == "max"):
                sub_ft_dict = self.get_max_dict(ini_data, sub_ft_data)
            elif(ptn_cond[ft_name] == "default"):
                sub_ft_dict = self.get_default_dict(ini_data, sub_ft_data)
            elif(ptn_cond[ft_name] == "ptnlist"):
                sub_ft_dict = self.get_ptnlist_dict(ini_data, sub_ft_data, a_ft_ptn_cnt)
            else:
                print "[__ERROR__] the attribute is not support"
            # print ">>>>>>>>>" + ft_name + " end<<<<<<<<"


            # update new pattern data
            for new_reg_key, new_val in sub_ft_dict.iteritems():
                rtn_data_dict[new_reg_key] = new_val


        return rtn_data_dict



if __name__ == '__main__':

    ptn_g = PtnGen_Manage()


    reg_data_dict = {
                      "rg_ft_node0"  : 20,
                      "rg_ft_node1"  : 20,
                      "rg_ft_node2"  : 20,
                      "rg_ft_node3"  : 20,
                      "rg_ft_node4"  : 20,
                      "rg_ft_node5"  : 20,
                      "rg_ft_node6"  : 20,
                      "rg_ft_node7"  : 20,
                      "rg_ft_node8"  : 20,
                      "rg_ft_node9"  : 20,
                      "rg_ft_node10" : 20,
                      "rg_ft_node11" : 20,
                      "rg_ft_node12" : 20,
                      "rg_ft_node13" : 20,
                      "rg_ft_node14" : 20,
                      "rg_ft_node15" : 20,
                      "rg_ft_node16" : 20,
                      "rg_ft_node17" : 20,
                      "rg_ft_node18" : 20,
                      "rg_ft_node19" : 20 }

    ft_flag_dict = {
                      "rg_ft_node0"  : 0,
                      "rg_ft_node1"  : 0,
                      "rg_ft_node2"  : 0,
                      "rg_ft_node3"  : 0,
                      "rg_ft_node4"  : 0,
                      "rg_ft_node5"  : 0,
                      "rg_ft_node6"  : 0,
                      "rg_ft_node7"  : 0,
                      "rg_ft_node8"  : 0,
                      "rg_ft_node9"  : 0,
                      "rg_ft_node10" : 0,
                      "rg_ft_node11" : 0,
                      "rg_ft_node12" : 0,
                      "rg_ft_node13" : 0,
                      "rg_ft_node14" : 0,
                      "rg_ft_node15" : 0,
                      "rg_ft_node16" : 0,
                      "rg_ft_node17" : 0,
                      "rg_ft_node18" : 0,
                      "rg_ft_node19" : 0 }

    # ptn_g.get_rand_sort_dict("ii[Idx]dd", [1,10], [0,255], False)

    ptn_g.update_lut_data( "rg_ft_node[Idx]", ft_flag_dict, reg_data_dict, [11,11,11,11,11,11,11,11,11,11,11,11] )

    pass
