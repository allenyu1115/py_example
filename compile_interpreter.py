'''
Created on 2021

@author: ayu
'''
from enum import Enum
from map_reduce_filter import get_key

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

'''
Can we just construct it into a monad, yes, we can 
,the state change can be hidden into a monad type
'''

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