import os
import sys
import re
import xlsxwriter
from collections import OrderedDict
import datetime
import json
from pprint import pprint



class TestGroupInfo(object):
    def __init__(self, group_name="", group_info={}, func_def=[]):

        self._group_name  = group_name
        self._group_info  = group_info
        self._func_def    = func_def

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    @property
    def group_info (self):
        return self._group_info

    @group_info .setter
    def group_info (self, value):
        self._group_info  = value

    @property
    def func_def(self):
        return self._func_def

    @func_def.setter
    def func_def(self, value):
        self._func_def = value


class TestGroup_Handle(object):
    def __init__(self, json_filename):

        self.TsetGroups_dict = self.TestGroups_Parse(json_filename)
        self.filename = json_filename

    def reset(self):
        self.TsetGroups_dict = self.TestGroups_Parse(self.filename)
        pass

    def TestGroups_Parse(self, a_json_file):

        tg_dict = OrderedDict()

        tg = json.load(open(a_json_file), object_pairs_hook=OrderedDict)

        for tg_name, tg_val in tg.iteritems():

            tg_info = TestGroupInfo("")

            tg_info.group_name = tg_name
            tg_info.group_info = tg_val["Group_Info"]
            tg_info.func_def   = tg_val["FuncDef"]

            tg_dict.update( {tg_name : tg_info} )

        return tg_dict

    def get_group_case_range_dict(self):
        rtn_dict = OrderedDict()
        for tg_key, tg_info in self.TsetGroups_dict.iteritems():
            rtn_dict[tg_key] = tg_info.group_info["Case_Range"]
        return rtn_dict

    def get_group_random_seed_dict(self):
        rtn_dict = OrderedDict()
        for tg_key, tg_info in self.TsetGroups_dict.iteritems():
            rtn_dict[tg_key] = tg_info.group_info["RandomSeed"]
        return rtn_dict

    def get_group_func_bypass_dict(self):
        rtn_dict = OrderedDict()
        for tg_key, tg_info in self.TsetGroups_dict.iteritems():
            rtn_dict[tg_key] = tg_info.group_info["FuncBypass"]
        return rtn_dict

    def get_group_info_dict(self):
        rtn_dict = OrderedDict()
        for tg_key, tg_info in self.TsetGroups_dict.iteritems():
            rtn_dict[tg_key] = tg_info.group_info
        return rtn_dict

    def get_funcdef_dict(self):
        rtn_dict = OrderedDict()
        for tg_key, tg_info in self.TsetGroups_dict.iteritems():
            rtn_dict[tg_key] = tg_info.func_def
        return rtn_dict



if __name__ == '__main__':

    json_file = "..\src\SPRefine_TestGroup.json"
    testgp_handle = TestGroup_Handle(json_file)

    test_1 = testgp_handle.get_funcdef_dict()
    for key, value in test_1.iteritems():
        print key, value
