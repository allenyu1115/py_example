'''
generated 10.28

@author: Allen Yu
'''
from enum import Enum
from pip._internal import self_outdated_check
    

def map_list(lst, func):
    rlst = []
    for l in lst:
        rlst.append(func(l)) 
    return rlst


def filter_list(lst, predict):
    rlst = []
    for l in lst:
        if predict(l):
            rlst.append(l)
    return rlst


def reduce_lst(lst, default, reduce_func):
    rst = default;
    for l in lst:
        rst = reduce_func(rst, l)
    return rst;


class CustomerizedList:
    def __init__(self,lst):
        self.lst = lst
        self.map_func_lst = []

    def map(self,map_func):
        self.map_func_lst.append(map_func)
        return self
    
    def clear_map_func(self):
        self.map_func_lst.clear()
        
    def execute(self): 
        rlst = []
        for i in self.lst:
            result = i
            for func in self.map_func_lst:
                result = func(result)
            rlst.append(result)
        return rlst

                
def reduce_recursive(lst, default, reduce_func): 
    if len(lst) == 0:
        return default
    elif len(lst) == 1:
        return reduce_func(default, lst[0])
    else:
        return reduce_func(lst[0], reduce_recursive(lst[1:], default, reduce_func))


# tail recursive equals iteration
def reduce_tail_recursive(lst, default, reduce_func):
    
    def inner(lst, last_value):
        return last_value if len(lst) == 0 else inner(lst[1:], reduce_func(last_value, lst[0]))
        
    return default if len(lst) == 0 else inner(lst, default)    

            
def group_by_lst(lst, group_by_key_func):
    rlst = map_list(lst, lambda x: (group_by_key_func(x), x))
    rdict = {}
    for key, i in rlst:
        value = rdict.get(key, [])
        value.append(i)
        rdict[key] = value   
    return rdict   


def get_key(x, group_by_condition):
        for cond, key in group_by_condition.items():
            if cond(x):
                return key


def test_map_reduce_filter():
    lst = [1, 3, 4, 6]  
    print(lst[0])   
    print(lst[1:])
    print(map_list(lst, lambda x: x + 1))
    print(filter_list(lst, lambda x: x > 3))  
    print(reduce_lst(lst, 10, lambda x, y: x + y)) 
    print(reduce_recursive(lst, 10, lambda x, y: x + y)) 
    print('tail recursive:' + str(reduce_tail_recursive(lst, 10, lambda x, y: x + y))) 
    
    group_by_condition = {lambda x: x < 18: 'under age', lambda x: x >= 18 and x < 30: 'young adult',
          lambda x: x >= 30 and x < 70: 'adult', lambda x: x >= 70: 'senior'}
    print(group_by_lst([('a', 12), ('b', 56), ('c', 34), ('c', 24), ('d', 70)], lambda x: get_key(x[1], group_by_condition)))


# tail recursive equals iteration
def check_list(lst, category_func):
    newLst = []

    def inner_check(lst, last_key, last_category):
        if len(lst) == 0:
            return newLst
        else: 
            ele = lst[0]   
            current_category = category_func(ele) 
            current_key = last_key if  current_category == last_category else last_key + 1         
            newLst.append((current_key, ele))
            return inner_check(lst[1:], current_key, current_category)
    
    return newLst if len(lst) == 0 else inner_check(lst, -1, category_func(lst[0]))


class CharType(Enum):
    operator_level = 1
    operator_level2 = 2
    undefine = 3
    blank = 4
    number = 5
    end = 6
    

char_type_condition = { lambda char:len(char) == 0: CharType.end,
                        lambda char: char.isspace(): CharType.blank,
                        lambda char: char.isnumeric(): CharType.number,
                        lambda char: char in ['+', '-']: CharType.operator_level,
                        lambda char: char in ['*', '/']: CharType.operator_level2,
                        lambda char: char: CharType.undefine  }


def default_compute(operator, left_num, right_num):
    return   '(' + operator + ' ' + left_num + ' ' + right_num + ')' if (left_num != '' and operator != '') else right_num

    
def get_s_exp_left_to_right(s, compute_func=default_compute):

    def get_s_inner(s, last_char_type, right_num, left_num, last_operator):
        current_char = '' if len(s) == 0 else s[0]
        char_type = get_key(current_char, char_type_condition)
        if(char_type == CharType.number):
            return get_s_inner(s[1:], char_type, right_num + current_char, left_num, last_operator);
        elif (char_type == CharType.operator_level or char_type == CharType.operator_level2):
            return get_s_inner(s[1:], char_type, '', compute_func(last_operator, left_num, right_num), current_char)
        elif (char_type == CharType.blank):
            return get_s_inner(s[1:], last_char_type, right_num, left_num, last_operator)
        elif (char_type == CharType.end):
            return compute_func(last_operator, left_num, right_num)
        else:
            return ''   
    
    return s if len(s) == 0 else get_s_inner(s, CharType.undefine, '', '', '')    


def get_s_expr(s, f_compute=default_compute):
    
    def sum_all(operator_stack, number_stack, default): 
           
        def inner(operator_stack, last_value):
            if len(operator_stack) == 0:
                return last_value
            else:
                return inner(operator_stack, f_compute(operator_stack.pop(), number_stack.pop(), last_value))
        
        return default if len(operator_stack) == 0 else inner(operator_stack, default)

    def get_s_expr_priority(s, right_num, number_stack, operator_stack):
        one_char = '' if len(s) == 0 else s[0]
        char_type = get_key(one_char, char_type_condition)
        if char_type == CharType.number:
            return get_s_expr_priority(s[1:], right_num + one_char, number_stack, operator_stack)
        elif char_type in [CharType.operator_level, CharType.operator_level2]:
            number_stack.append((right_num if get_key(operator_stack[-1], char_type_condition).value < char_type.value 
                                    else sum_all(operator_stack, number_stack, right_num))  if  len(operator_stack) != 0 else right_num)                
            operator_stack.append(one_char)
            return get_s_expr_priority(s[1:], '', number_stack, operator_stack)
        elif (char_type == CharType.blank):
            return get_s_expr_priority(s[1:], right_num, number_stack, operator_stack)
        elif (char_type == CharType.end):
            return sum_all(operator_stack, number_stack, right_num)
        
    return s if len(s) == 0 else get_s_expr_priority(s, '', [], [])
    
    
if __name__ == '__main__':
    
    print(CustomerizedList([1,2,6,4]).map(lambda x: x + 1).map(lambda x: x*2).execute())
    test_map_reduce_filter()
    test_str = 'ab123b23cdd432a'
    
    grp_lst = group_by_lst(check_list(test_str, lambda x: x.isalpha()), lambda x:x[0])
    rlst = []
    for key, value in grp_lst.items():
        mapped_lst = map_list(value, lambda x: x[1])
        reduce_value = reduce_lst(mapped_lst, '', lambda x , y: x + y)
        rlst.append(reduce_value)
    print(rlst)
    
    original = '71 + 8 * 96 - 899 - 85 + 8 / 4 '
    operatorFunc = {'+':lambda x, y: x + y,
                    '-':lambda x, y: x - y,
                    '*':lambda x, y: x * y,
                    '/': lambda x, y: x / y }
    
    def  compute(operator, left_num, right_num):
        if  left_num != '' and operator != '':
            return operatorFunc.get(operator)(int(left_num), int(right_num))
        else:
            return right_num 
        
    print(get_s_exp_left_to_right(original))
    print(get_s_expr(original))
    print(get_s_exp_left_to_right(original, compute))
    print(get_s_expr(original, compute))

