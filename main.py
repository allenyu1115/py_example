'''
generated 10.28

@author: Allen Yu
'''
from enum import Enum
    

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


def reduce_recursive(lst, default, reduce_func): 
    if len(lst) == 0:
        return default
    elif len(lst) == 1:
        return reduce_func(default, lst[0])
    else:
        return reduce_func(lst[0], reduce_recursive(lst[1:], default, reduce_func))


# tail recursive equals iteration
def reduce_tail_recursive(lst, default, reduce_func):
    
    def inner(lst, last_value, reduce_func):
        if len(lst) == 0:
            return last_value
        else:
            reduceValue = reduce_func(last_value, lst[0])
            return inner(lst[1:], reduceValue, reduce_func)
        
    if len(lst) == 0:
        return default
    
    return inner(lst, default, reduce_func)    

            
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


def test():
    lst = [1, 3, 4, 6]
    
    print(lst[0])   
    print(lst[1:])
    print(map_list(lst, lambda x: x + 1))
    print(filter_list(lst, lambda x: x > 3))  
    print(reduce_lst(lst, 10, lambda x, y: x + y)) 
    print(reduce_recursive(lst, 10, lambda x, y: x + y)) 
    print('tail:' + str(reduce_tail_recursive(lst, 10, lambda x, y: x + y))) 
    
    group_by_condition = {lambda x: x < 18: 'under age', lambda x: x >= 18 and x < 30: 'young adult',
          lambda x: x >= 30 and x < 70: 'adult', lambda x: x >= 70: 'senior'}
    print(group_by_lst([('a', 12), ('b', 56), ('c', 34), ('c', 24), ('d', 70)], lambda x: get_key(x[1], group_by_condition)))


# tail recursive equals iteration
def check_list(lst, category_func):
    newLst = []

    def inner_check(lst, last_key, last_category , category_func):
        if len(lst) == 0:
            return newLst
        else: 
            ele = lst[0]   
            current_category = category_func(ele) 
            current_key = last_key if  current_category == last_category else last_key + 1         
            newLst.append((current_key, ele))
            return inner_check(lst[1:], current_key, current_category, category_func)
    
    if len(lst) == 0:
        return newLst
    
    return inner_check(lst, -1, category_func(lst[0]), category_func)


class CharType(Enum):
    operator = 1
    number = 2
    undefine = 3
    blank = 4
    end = 5
    
    
class CharTypePriority(Enum):
    operator_level = 1
    operator_level2 = 2
    undefine = 3
    blank = 4
    number = 5
    end = 6

    
char_type_condition = { lambda char:len(char) == 0: CharType.end,
                        lambda char: char.isspace(): CharType.blank,
                        lambda char: char.isnumeric(): CharType.number,
                        lambda char: char in ['+', '-', '*', '/']: CharType.operator,
                        lambda char: char: CharType.undefine  }
       

def  default_compute(operator, left_num, right_num):
    return   '(' + operator + ' ' + left_num + ' ' + right_num + ')' if (left_num != '' and operator != '') else right_num

    
def get_s_expression(s, compute_func=default_compute):

    def get_s_inner(s, last_char_type, right_num, left_num, last_operator, combine_f):
        current_char = '' if len(s) == 0 else s[0]
        char_type = get_key(current_char, char_type_condition)
        if(char_type == CharType.number):
            return get_s_inner(s[1:], char_type, right_num + current_char, left_num, last_operator, combine_f);
        elif (char_type == CharType.operator):
            return get_s_inner(s[1:], char_type, '', combine_f(last_operator, left_num, right_num), current_char, combine_f)
        elif (char_type == CharType.blank):
            return get_s_inner(s[1:], last_char_type, right_num, left_num, last_operator, combine_f)
        elif (char_type == CharType.end):
            return combine_f(last_operator, left_num, right_num)
        else:
            return ''   

    if len(s) == 0:
        return s
    else:
        return get_s_inner(s, CharType.undefine, '', '', '', compute_func)    

    
char_type_priority_condition = { lambda char:len(char) == 0: CharTypePriority.end,
                        lambda char: char.isspace(): CharTypePriority.blank,
                        lambda char: char.isnumeric(): CharTypePriority.number,
                        lambda char: char in ['+', '-']: CharTypePriority.operator_level,
                        lambda char: char in ['*', '/']: CharTypePriority.operator_level2,
                        lambda char: char: CharTypePriority.undefine  }


def get_s_expr(s, f_compute=default_compute):

    def get_s_expr_priority(s, right_num, number_stack, operator_stack, f_compute):
        one_char = '' if len(s) == 0 else s[0]
        char_type = get_key(one_char, char_type_priority_condition)
        if char_type == CharTypePriority.number:
            return get_s_expr_priority(s[1:], right_num + one_char, number_stack, operator_stack, f_compute)
        elif char_type in [CharTypePriority.operator_level, CharTypePriority.operator_level2]:
            if len(operator_stack) != 0:
                top_operator = operator_stack[-1]
                top_operator_char_type = get_key(top_operator, char_type_priority_condition)
                if top_operator_char_type.value < char_type.value:
                    number_stack.append(right_num)
                else:
                    sum_num = right_num
                    while len(operator_stack) != 0:
                        current_operator = operator_stack.pop()
                        sum_num = f_compute(current_operator, number_stack.pop(), sum_num) 
                    number_stack.append(sum_num)
            else:
                number_stack.append(right_num)                
            operator_stack.append(one_char)
            return get_s_expr_priority(s[1:], '', number_stack, operator_stack , f_compute)
        elif (char_type == CharTypePriority.blank):
            return get_s_expr_priority(s[1:], right_num, number_stack, operator_stack, f_compute)
        elif (char_type == CharTypePriority.end):
            sum_num = right_num
            while len(operator_stack) != 0:
                current_operator = operator_stack.pop()
                sum_num = f_compute(current_operator, number_stack.pop(), sum_num) 
            return sum_num
        
    if len(s) == 0:
        return s
    else:
        return get_s_expr_priority(s, '', [], [], f_compute)
    
    
if __name__ == '__main__':
    testString = 'ab123b23cdd432a'
    x = group_by_lst(check_list(testString, lambda x: x.isalpha()), lambda x:x[0])
    for key, value in x.items():
        y = map_list(value, lambda x: x[1])
        z = reduce_lst(y, '', lambda x , y: x + y)
        print(z)
    test()
    original = '71 + 8 * 96 - 899 - 85'
    print(get_s_expression(original))
    print(get_s_expr(original))
    operatorFunc = {'+':lambda x, y: x + y,
                    '-':lambda x, y: x - y,
                    '*':lambda x, y: x * y,
                    '/': lambda x, y: x / y }

    def  compute(operator, left_num, right_num):
        if  left_num != '' and operator != '':
            return operatorFunc.get(operator)(int(left_num), int(right_num))
        else:
            return right_num       

    print(get_s_expression(original, compute))
    print(get_s_expr(original, compute))

