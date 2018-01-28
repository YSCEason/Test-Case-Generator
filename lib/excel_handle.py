import os
import sys
import re
import xlsxwriter
import datetime
from collections import OrderedDict

class Excel_Handle(object):
    def __init__(self, filename):

        self.wb              = self.initial_excel(filename)
        self.tg_reglist_dict = OrderedDict()
        pass

    def reset(self):
        self.tg_reglist_dict = OrderedDict()
        pass

    def initial_excel(self, a_filename):

        workbook = xlsxwriter.Workbook(a_filename)

        return workbook

    def create_group_sheet(self, a_group_name, a_ft_list, a_ini_data, a_ft_data):

        sheet = self.wb.add_worksheet(a_group_name)

        self.join_reg_to_title_base_on_subfunc(a_ft_list, a_ini_data, a_ft_data)
        self.write_title_to_sheet(sheet)

        return sheet

    def join_reg_to_title_base_on_subfunc(self, a_ft_name_list, a_ini_data, a_ft_data):

        ft_list   = a_ft_name_list
        ft_data   = a_ft_data
        ini_data  = a_ini_data

        ft_reg_list = []

        for _ft_name in ft_list:
            reg_list = []
            for reg_name in ft_data[_ft_name]:
                reg_list.append(reg_name)

            self.tg_reglist_dict.update( {_ft_name : reg_list} )

    def write_title_to_sheet(self, a_worksheet):

        _ex_gp_dict = self.tg_reglist_dict
        worksheet   = a_worksheet

        reg_format = self.wb.add_format()
        reg_format.set_rotation(-90)
        reg_format.set_bold()

        gp_format = self.wb.add_format()
        gp_format.set_bold()
        gp_format.set_align("center")

        gp_row  = 1
        reg_row = 2
        reg_col = 1

        for gp_key, gp_val in _ex_gp_dict.iteritems():
            # write title for function name
            mg_first_col = reg_col
            mg_last_col  = reg_col+len(gp_val)-1
            worksheet.merge_range(gp_row, mg_first_col, gp_row, mg_last_col, gp_key, gp_format)

            for reg_name in gp_val:
                # write title for register name
                worksheet.write(reg_row, reg_col, reg_name, reg_format)
                reg_col += 1

    def write_data_to_sheet(self, a_worksheet, a_ini_data, a_CaseIdx):

        _ex_gp_dict = self.tg_reglist_dict

        worksheet = a_worksheet
        ini_data  = a_ini_data
        CaseIdx   = a_CaseIdx

        worksheet.set_column('A:A', 13)

        # write the test case
        col = 1
        for gp_key, gp_val in _ex_gp_dict.iteritems():
            for reg_name in gp_val:
                worksheet.write(2+CaseIdx, 0, "pattern_" + "%05d"%CaseIdx)
                worksheet.write(2+CaseIdx, col, ini_data[reg_name])
                col += 1

    def close(self):
        self.wb.close()
        pass


if __name__ == '__main__':

    pass
