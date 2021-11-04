'''
generated 10.28

@author: Allen Yu
'''
from enum import Enum


class CharType(Enum):
    operator = 1
    number = 2
    undefine = 3
    blank = 4
    end = 5


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


char_type_condition = { lambda char:len(char) == 0: CharType.end,
                            lambda char: char.isspace(): CharType.blank,
                            lambda char: char.isnumeric(): CharType.number,
                            lambda char: char in ['+', '-', '*', '/']: CharType.operator,
                            lambda char: char: CharType.undefine  }
       
def get_s_expression(s):
    def get_s_expression_recursive(s, last_char_type, current_num, last_num, last_operator, combine_f):
        current_char = '' if len(s) == 0 else s[0]
        charType = get_key(current_char, char_type_condition)
        if(charType == CharType.number):
            return get_s_expression_recursive(s[1:], charType, current_num + current_char, last_num, last_operator, combine_f);
        elif (charType == CharType.operator):
            return get_s_expression_recursive(s[1:], charType, '', combine_f(last_operator, last_num, current_num), current_char, combine_f)
        elif (charType == CharType.blank):
            return get_s_expression_recursive(s[1:], last_char_type, current_num, last_num, last_operator, combine_f)
        elif (charType == CharType.end):
            return combine_f(last_operator, last_num, current_num)
        else:
            return ''   

    if len(s) == 0:
        return s
    else:
        return get_s_expression_recursive(s, CharType.undefine, '', '', '',
                                          lambda operator, left_num, right_num: 
                                              '(' + operator + ' ' + left_num + ' ' + right_num + ')' if (left_num != '' and operator != '') 
                                               else right_num)    


if __name__ == '__main__':
    testString = 'ab123b23cdd432a'
    x = group_by_lst(check_list(testString, lambda x: x.isalpha()), lambda x:x[0])
    for key, value in x.items():
        y = map_list(value, lambda x: x[1])
        z = reduce_lst(y, '', lambda x , y: x + y)
        print(z)
    test()
    xx = get_s_expression('71 + 8 * 76 - 899 + 5')
    print(xx)

