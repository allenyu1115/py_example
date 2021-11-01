'''
generated 10.28

@author: Allen Yu
'''


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
    if len(lst) == 1:
        return reduce_func(default, lst[0])
    elif len(lst) > 1:
        return reduce_func(lst[0], reduce_recursive(lst[1:], default, reduce_func))
    else:
        return default;

            
def group_by_lst(lst, group_by_key_func):
    rlst = map_list(lst, lambda x: (group_by_key_func(x), x))
    rdict = {}
    for key, i in rlst:
        value = rdict.get(key, [])
        value.append(i)
        rdict[key] = value   
    return rdict   


def test():
    lst = [1, 3, 4, 6]
    
    print(lst[0])   
    print(lst[1:])
    print(map_list(lst, lambda x: x + 1))
    print(filter_list(lst, lambda x: x > 3))  
    print(reduce_lst(lst, 10, lambda x, y: x + y)) 
    print(reduce_recursive(lst, 10, lambda x, y: x + y)) 
    
    group_by_condition = {lambda x: x < 18: 'under age', lambda x: x >= 18 and x < 30: 'young adult',
          lambda x: x >= 30 and x < 70: 'adult', lambda x: x >= 70: 'senior'}
    
    def get_key(x):
        for cond, key in group_by_condition.items():
            if cond(x):
                return key

    print(group_by_lst([('a', 12), ('b', 56), ('c', 34), ('c', 24), ('d', 70)], lambda x: get_key(x[1])))


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
       
    
if __name__ == '__main__':
    testString = 'ab123b23cdd432a'
    x = group_by_lst(check_list(testString, lambda x: x.isalpha()), lambda x:x[0])
    for key, value in x.items():
        y = map_list(value, lambda x: x[1])
        z = reduce_lst(y, '', lambda x , y: x + y)
        print(z)
    test()

