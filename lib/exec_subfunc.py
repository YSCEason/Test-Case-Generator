import random
import ast
from pprint import pprint


# =========== get pattern  =============

def _max(arg1, arg2, *args):
    return max(arg1, arg2, *args)

def _min(arg1, arg2, *args):
    return min(arg1, arg2, *args)

def _randint(a_start, a_end):
    return random.randint(a_start, a_end)

def _randlist(a_list):
    return random.choice(a_list)

def _rand_align(a_start, a_end, a_align):
    ss = _align_ceil(a_start, a_align)
    return random.randrange( ss, a_end+1, a_align )

def _align_ceil(a_val, a_align):
    return ((( a_val + (a_align-1) ) / a_align) * a_align)

def _align_floor(a_val, a_align):
    return (a_val / a_align * a_align)

def _rand_even(a_start, a_end):
    ss = _align_ceil(a_start, 2)
    return random.randrange( ss, a_end+1, 2 )

def _rand_odd(a_start, a_end):
    ss = a_start if (a_start % 2) else (a_start+1)
    odd = random.randrange( ss, a_end+1, 2 )
    return odd

def _max_bits(a_bitnum):
    return (2 ** a_bitnum) - 1

def _lut_sort_incre(a_idx_range, a_val_range):
    random_list = list()
    sort_list   = list()

    for ii in range(a_idx_range[0], a_idx_range[1]+1):
        rand_tmp = random.randint(a_val_range[0], a_val_range[1])
        random_list.append( rand_tmp )

    sort_list = sorted(random_list)

    return sort_list


def _lut_sort_desc(a_idx_range, a_val_range):
    random_list = list()
    sort_list   = list()

    for ii in range(a_idx_range[0], a_idx_range[1]+1):
        rand_tmp = random.randint(a_val_range[0], a_val_range[1])
        random_list.append( rand_tmp )

    sort_list = sorted(random_list, key=int, reverse=True)

    return sort_list


def _lut_sort_incre_align(a_idx_range, a_val_range, a_align):
    random_list = list()
    sort_list   = list()

    for ii in range(a_idx_range[0], a_idx_range[1]+1):
        rand_tmp = _rand_align(a_val_range[0], a_val_range[1], a_align)
        random_list.append( rand_tmp )

    sort_list = sorted(random_list)

    return sort_list

def _lut_sort_desc_align(a_idx_range, a_val_range, a_align):
    random_list = list()
    sort_list   = list()

    for ii in range(a_idx_range[0], a_idx_range[1]+1):
        rand_tmp = _rand_align(a_val_range[0], a_val_range[1], a_align)
        random_list.append( rand_tmp )

    sort_list = sorted(random_list, key=int, reverse=True)

    return sort_list

def _lut_rand(a_idx_range, a_val_range):
    random_list = list()

    for ii in range(a_idx_range[0], a_idx_range[1]+1):
        rand_tmp = random.randint(a_val_range[0], a_val_range[1])
        random_list.append( rand_tmp )

    return random_list

def _lut_rand_align(a_idx_range, a_val_range, a_align):
    random_list = list()

    for ii in range(a_idx_range[0], a_idx_range[1]+1):
        rand_tmp = _rand_align(a_val_range[0], a_val_range[1], a_align)
        random_list.append( rand_tmp )

    return random_list


# =========== check limitation  =============

def _check_align(a_reg, a_align):
    return ( a_reg % a_align == 0 )

def _check_even(a_reg):
    return ( a_reg % 2 == 0 )

def _check_odd(a_reg):
    return ( (a_reg+1) % 2 == 0 )






if __name__ == '__main__':

    print " _max                  = ",  _max(4,2,82,100,22)
    print " _min                  = ",  _min(5,6,82,20)
    print " _randint              = ",  _randint(0, 10)
    print " _randlist             = ",  _randlist([0,15,12])
    print " _rand_align           = ",  _rand_align(5, 20, 5)
    print " _rand_even            = ",  _rand_even(5, 6)
    print " _rand_odd             = ",  _rand_odd(4, 5)
    print " _max_bits             = ",  _max_bits(5)
    print " _align_ceil           = ",  _align_ceil(10,6)
    print " _align_floor          = ",  _align_floor(10,4)
    print

    print " _lut_sort_incre       = ",  _lut_sort_incre([0,10],[0,255])
    print " _lut_sort_desc        = ",  _lut_sort_desc([0,10],[0,255])
    print " _lut_sort_incre_align = ",  _lut_sort_incre_align([0,10],[0,255], 5)
    print " _lut_sort_desc_align  = ",  _lut_sort_desc_align([0,10], [0,255], 3)
    print " _lut_rand             = ",  _lut_rand([0,10],[0,255])
    print " _lut_rand_align       = ",  _lut_rand_align([0,10],[0,255], 7)
    print

    pass
