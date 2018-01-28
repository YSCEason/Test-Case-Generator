import os
import sys
import re
import xlsxwriter
from collections import OrderedDict
import datetime
import json
from pprint import pprint

from lib.initfile_handle  import InitFile_Handle
from lib.funcdef_handle   import FuncDef_Handle
from lib.testgroup_handle import TestGroup_Handle
from lib.excel_handle     import Excel_Handle
from lib.ptngen_manage    import PtnGen_Manage
from lib.check_limitation import Check_Limitation


class Generator_Main(object):
    def __init__(self):

        self.src_path      = ".\src\Sample_SR"
        self.src_init      = os.path.join(self.src_path, "sp_refine_a_init.txt")
        self.src_func_def  = os.path.join(self.src_path, "SPRefine_FuncDef.json")
        self.src_test_gp   = os.path.join(self.src_path, "SPRefine_TestGroup.json")

        self.out_path      = ".\CGOut"
        self.out_init      = "sp_refine_a_init.txt"
        self.out_xlsx      = os.path.join(self.out_path, "sp_refine.xlsx")



        self.ini_data      = InitFile_Handle(self.src_init)
        self.ft_data       = FuncDef_Handle(self.src_func_def)
        self.tg_data       = TestGroup_Handle(self.src_test_gp)
        self.excel_handle  = Excel_Handle(self.out_xlsx)
        self.ptngen        = PtnGen_Manage()
        self.chk_limit     = Check_Limitation()


    def main(self):

        _tg_data  = self.tg_data.get_group_info_dict()

        for tg_name, tg_info in _tg_data.iteritems():

            self.excel_handle.reset()
            self.ini_data.reset()
            self.ft_data.reset()

            _ini_data     = self.ini_data.get_value_dict()
            _ini_bit_num  = self.ini_data.get_bit_number_dict()
            _ft_data      = self.ft_data.get_all_func_def_dict()

            # update ft_data for the non-define attribute
            self.ft_data.update_non_def_reg_attribute(_ini_bit_num, _ini_data)

            # -------------  [Init File] Check output folder  -------------
            tg_path = os.path.join(self.out_path, tg_name)
            if not os.path.exists(tg_path):
                os.makedirs(tg_path)
            # ------------------------------------------

            # [Excel] create test group sheet
            xlsx_sheet = self.excel_handle.create_group_sheet(tg_name, tg_info["Out_title"], _ini_data, _ft_data)

            # Get func_def condition from tg_data
            tg_func_def_list = self.tg_data.get_funcdef_dict()

            ft_def_cnt = 0
            for case_idx in range(tg_info["Case_Range"][0], tg_info["Case_Range"][1]+1):

                ft_def_idx, ft_def_cnt = self.get_ft_def_idx(case_idx, tg_info["FuncDef_Num"])

                new_pattern_dict = OrderedDict()

                # ===== get pattern =====
                new_pattern_dict = self.ptngen.get_pattern_dict( tg_func_def_list[tg_name][ft_def_idx], ft_def_cnt, _ini_data, _ft_data, (case_idx+tg_info["RandomSeed"]) )

                # ===== update func bypass =====
                self.update_func_bypass_reg(tg_info, new_pattern_dict)

                # ===== check limitation =====
                self.chk_limit.check_reg_limitation(case_idx, new_pattern_dict, _ft_data)

                # ===== update initial file =====
                self.ini_data.update_value_dict( new_pattern_dict )
                _ini_data = self.ini_data.get_value_dict()



                # -------------  output file  -------------
                pattern_path = os.path.join( ("%s\pattern_%05d")%(tg_path, case_idx) )

                if not os.path.exists(pattern_path):
                    os.makedirs(pattern_path)

                Out_filename = os.path.join(pattern_path, self.out_init)
                self.ini_data.Write_data_to_InitFile(Out_filename)               # [Init File] write data
                self.excel_handle.write_data_to_sheet(xlsx_sheet, _ini_data, case_idx)  # [Excel] write data
                # -----------------------------------------


        # [Excel] close workbook
        self.excel_handle.close()
        pass

    def update_func_bypass_reg(self, a_tg_info, a_new_pattern_dict):

        tg_info = a_tg_info
        new_pattern_dict = a_new_pattern_dict

        for reg_name, reg_val in tg_info["FuncBypass"].iteritems():
            new_pattern_dict[reg_name] = reg_val

        pass

    def get_ft_def_idx(self, a_case_idx, a_ft_num_list):

        ft_num_list = a_ft_num_list
        ft_idx = 0
        case_idx = a_case_idx

        ft_str_list = []
        start_num = 1

        ii = 0
        while ii < len(ft_num_list):
            ft_str_list.append(start_num)
            start_num += ft_num_list[ii]
            ii += 1

        jj = 1
        while jj < len(ft_str_list):
            if not (case_idx < ft_str_list[jj]):
                ft_idx += 1
            jj += 1

        ft_cnt = a_case_idx-ft_str_list[ft_idx]

        return ft_idx, ft_cnt



if __name__ == '__main__':

    casegen = Generator_Main()
    casegen.main()

    pass

