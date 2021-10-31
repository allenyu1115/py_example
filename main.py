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

        

def split_lst(lst,key_func):
    def inner_recursive(lst,last_element, position, keyfunc, position_increase_func, newLst):
        if len(lst) == 0:
            return newLst
        else:
            current_element = lst[0]
            current_key = keyfunc(current_element)
            last_key = keyfunc(last_element)
            if current_key == position_increase_func(last_key):
                current_key = last_key
            newLst.append( (position, current_key, current_element) )
            return inner_recursive( lst[1:],  current_element, position_increase_func(position), keyfunc, position_increase_func, newLst )  
         
    if len(lst) == 0:
        return lst
    else:
        return inner_recursive(lst,lst[0], 0,key_func,lambda x: x + 1, [] )
    
if __name__ == '__main__':
    testString='ab123b23cdd432a'
    test()

