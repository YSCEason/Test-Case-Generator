import os
import sys
import re
import xlsxwriter
from collections import OrderedDict
import datetime
import json
from pprint import pprint



class FuncDefInfo(object):
    def __init__(self, name):
        self._func_name   = {}
        self._reg_info    = OrderedDict()
            # {
            #     "LutIdxRange"  : [0, 20],
            #     "Constant"     : 45,
            #     "max"          : 255,
            #     "min"          : 0,
            #     "ind_method"   : "",
            #     "corr_method"  : "sort_incre([0,20], Rand(0, 25))",
            #     "constraint"   : ["align(8)"] }
            # }

    @property
    def func_name(self):
        return self._func_name

    @func_name.setter
    def func_name(self, value):
        self._func_name = value

    @property
    def reg_info(self):
        return self._reg_info

    @reg_info.setter
    def reg_info(self, value):
        self._reg_info = value



class FuncDef_Handle(object):
    def __init__(self, json_filename):

        self.FuncDef_dict = self.FuncDef_Parse(json_filename)
        self.filename = json_filename

    def reset(self):
        self.FuncDef_dict = self.FuncDef_Parse(self.filename)
        pass

    def FuncDef_Parse(self, a_json_file):

        func_dict = OrderedDict()
        func_defs = json.load(open(a_json_file), object_pairs_hook=OrderedDict)

        for ft_name, reg_info in func_defs.iteritems():

            ft_def_info = FuncDefInfo("")
            _reg_info_dict = OrderedDict()

            ft_def_info.func_name = ft_name

            for reg_key, reg_constr in reg_info.iteritems():

                # ---------- Check lut table idx ----------
                if "[Idx]" in reg_key:
                    # if the register is LUT
                    ii_s = reg_constr["LutIdxRange"][0]
                    ii_e = reg_constr["LutIdxRange"][1]

                    for ii in range(ii_s, ii_e+1):
                        reg_name = reg_key.replace("[Idx]", str(ii))
                        _reg_info_dict[reg_name] = self.get_reg_attribute(reg_constr)
                        _reg_info_dict[reg_name]["keyword"] = reg_key

                        const_list = []
                        for const in _reg_info_dict[reg_name]["constraint"]:
                            const_list.append( const.replace("[Idx]", str(ii)) )
                        _reg_info_dict[reg_name]["constraint"] = const_list
                else:
                    # the register is not LUT
                    reg_name = reg_key
                    _reg_info_dict[reg_name] = self.get_reg_attribute(reg_constr)
                # -------------------------------------------


            ft_def_info.reg_info = _reg_info_dict

            func_dict.update( {ft_name : ft_def_info} )

        return func_dict

    def get_all_func_def_dict(self):
        rtn_dict = {}
        for ft_key, ft_info in self.FuncDef_dict.iteritems():
            rtn_dict[ft_key] = ft_info.reg_info
        return rtn_dict

    def get_subfunc_dict(self, a_func_name):
        rtn_dict = {}
        rtn_dict = self.FuncDef_dict[a_func_name].reg_info
        return rtn_dict

    def get_reg_attribute(self, a_reg_constr):

        reg_constr = a_reg_constr

        _reg_constr_dict = OrderedDict()
        _reg_constr_dict = { "LutIdxRange": [],
                             "constant"   : "",
                             "max"        : "",
                             "min"        : "",
                             "ind_method" : "",
                             "corr_method": "",
                             "ptnlist"    : [],
                             "user_def"   : [],
                             "constraint" : [],
                             "keyword"    : ""  }

        for const_key in _reg_constr_dict.keys():
            if not reg_constr.has_key(const_key):
                _reg_constr_dict[const_key] = "__No_Def__"
            elif not reg_constr[const_key]:
                _reg_constr_dict[const_key] = "__No_Def__"
            elif (isinstance(reg_constr[const_key], str) and (reg_constr[const_key] == "")):
                _reg_constr_dict[const_key] = "__No_Def__"
            elif (isinstance(reg_constr[const_key], list) and len(reg_constr[const_key]) == 0):
                _reg_constr_dict[const_key] = "__No_Def__"
            else:
                _reg_constr_dict[const_key] = reg_constr[const_key]

        # print reg_key, _reg_constr_dict

        return _reg_constr_dict

    def update_non_def_reg_attribute(self, a_ini_bitnum_dict, a_ini_data_dict):

        bit_num_dict  = a_ini_bitnum_dict
        ini_data_dict = a_ini_data_dict

        for ft_key, ft_info in self.FuncDef_dict.iteritems():
            for reg_key, reg_info in ft_info.reg_info.iteritems():
                if (reg_info["max"] == "__No_Def__") :
                    reg_info["max"] = str((2 ** bit_num_dict[reg_key]) - 1)
                if (reg_info["min"] == "__No_Def__"):
                    reg_info["min"] = str(0)
                if (reg_info["constant"] == "__No_Def__") :
                    reg_info["constant"] = str(ini_data_dict[reg_key])

                # print ("%20s \t:\t %s")%(reg_key, reg_info)
            # print ("^^^ %20s ^^^")%(ft_key)
            # print
            # print
        # pass

if __name__ == '__main__':

    funcdef_handle = FuncDef_Handle("..\src\SPRefine_FuncDef.json")

    ft_info = funcdef_handle.get_all_func_def_dict()

    # for key, info in ft_info.iteritems():
    #     print key
    #     for reg_key, reg_info in info.iteritems():
    #         print ("\t\t (%s)")%(reg_key)
    #         for con_key, con_info in reg_info.iteritems():
    #             print ("\t\t\t\t\t >>>> ((%10s)) \t\t::   %s")%(con_key, con_info)


    # sub_ft_info = funcdef_handle.get_subfunc_dict("Common")
    # print sub_ft_info

    # funcdef_handle.update_non_def_min_and_max( {"rg_o2o_diff_th": 2} )
