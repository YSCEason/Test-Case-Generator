import re
from collections import OrderedDict
import datetime


class RegInfo(object):
    def __init__(self, reg_name="", bit_num=16, base='h', sw_config='Y', value=0):
        self._reg_name  = reg_name
        self._bit_num   = bit_num
        self._base      = base
        self._sw_config = sw_config
        self._value     = value

    @property
    def reg_name(self):
        return self._reg_name

    @reg_name.setter
    def reg_name(self, value):
        self._reg_name = value

    @property
    def bit_num(self):
        return self._bit_num

    @bit_num.setter
    def bit_num(self, value):
        self._bit_num = value

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

    @property
    def sw_config(self):
        return self._sw_config

    @sw_config.setter
    def sw_config(self, value):
        self._sw_config = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class InitFile_Handle(object):
    def __init__(self, filename):

        self.RegInfo_dict = self.InitFile_Parse(filename)
        self.filename = filename

    def reset(self):
        self.RegInfo_dict = self.InitFile_Parse(self.filename)
        pass

    def InitFile_Parse(self, a_filename):
        reg_dict = OrderedDict()
        sw_config = "N"

        with open(a_filename, 'r') as f:
            for line in f:

                reg_info = RegInfo("")
                match = re.search(r"^(\w+)(\s*=\s*)(\d+)(')([dDhH])([\da-fA-F]+)", line, 0)

                if match:
                    reg_info.reg_name = match.group(1)

                    if match.group(5) in ['d', 'D']:
                        value_string = r'{}'.format(match.group(6))
                        reg_info.data = int(value_string, base = 10)
                    elif match.group(5) in ['h', 'H']:
                        value_string = r'0x{}'.format(match.group(6))
                        reg_info.data = int(value_string, base = 16)

                    reg_info.bit_num    = int(match.group(3))
                    reg_info.symbol     = match.group(5)
                    reg_info.sw_config  = sw_config

                    reg_dict.update( {reg_info.reg_name : reg_info} )

                else:
                    match = re.search(r"(SW_CONFIG)", line, 0)
                    if match:
                        sw_config = "Y"

        return reg_dict

    def get_value_dict(self):
        rtn_dict = dict()
        for key, reg in self.RegInfo_dict.items():
            rtn_dict[key] = reg.data
        return rtn_dict

    def get_bit_number_dict(self):
        rtn_dict = dict()
        for key, reg in self.RegInfo_dict.items():
            rtn_dict[key] = reg.bit_num
        return rtn_dict

    def update_value_dict(self, new_dict):
        for key, value in new_dict.items():
            if key in self.RegInfo_dict.keys():
                self.RegInfo_dict[key].data = value

    def Write_data_to_InitFile(self, a_out_filename):

        reg_dict = self.RegInfo_dict
        sw_idx = 1

        with open(a_out_filename, 'w') as f:
            for reg_name, reg_info in reg_dict.iteritems():

                if ("Y"== reg_info.sw_config and sw_idx==1):
                    f.write("\n")
                    f.write("SW_CONFIG\n")
                    sw_idx=0

                if reg_info.symbol in ['d', 'D']:
                    out_str = ("%s = %s'%s%d\n") % (reg_info.reg_name, reg_info.bit_num, reg_info.base, reg_info.data )
                elif reg_info.symbol in ['h', 'H']:
                    out_str = ("%s = %s'%s%x\n") % (reg_info.reg_name, reg_info.bit_num, reg_info.base, reg_info.data )

                f.write(out_str)

            f.write("\n")
            f.write("end_of_file")


if __name__ == '__main__':

    inifile_handle = InitFile_Handle("..\src\sp_refine_a_init.txt")

    for key, value in inifile_handle.get_value_dict().iteritems():
        print key, value

    # for key, value in inifile_handle.get_bit_number_dict().iteritems():
        # print key, value

    # inifile_handle.update_value_dict({"rg_prev_sel" : 20, "rg_rt_upd_req":55})

    # for key, value in inifile_handle.get_value_dict().iteritems():
    #     if (key == "rg_rt_upd_req" or key == "rg_prev_sel"):
    #         print key, value

    inifile_handle.Write_data_to_InitFile("..\CaseGen_output\output.txt")

    pass
