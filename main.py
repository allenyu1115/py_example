'''

@author: ayu
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


def reduce_recusive(lst, default, reduce_func):
    if len(lst) == 0:
        return default
    elif len(lst) == 1:
        return reduce_func(default, lst[0])
    elif len(lst) > 1:
        return reduce_func(lst[0], reduce_recusive(lst[1:], default, reduce_func))

    
if __name__ == '__main__':
    lst = [1, 3, 4, 6]
    print(lst[0])
    print(lst[1:])
    print(map_list(lst, lambda x: x + 1))
    print(filter_list(lst, lambda x: x > 3))  
    print(reduce_lst(lst, 10, lambda x, y: x + y)) 
    print(reduce_recusive(lst, 10, lambda x, y: x + y))      
