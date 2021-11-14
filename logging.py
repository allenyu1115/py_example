'''
Created on Nov 14, 2021

@author: Allen Yu
'''

islogging = True

'''
class version
'''


class LoggingBase:

    def __getattribute__(self, item):
        attr = super(LoggingBase, self).__getattribute__(item)

        def decorate_func(*args):
            print('-----------log input parameter')
            print('class :' + str(self) + ';method:' + str(attr.__func__))
            for arg in args:
                print('parameter: ' + arg)
            print('----------end log input parameter')
            rval = attr.__func__(self, *args)
            print('----------the result log:' + str(rval))
            return rval

        return decorate_func if islogging is True else attr

    
class MyClass2(LoggingBase):

    def __init__(self, a):
        self.a = a
        
    def print_me(self, b, x):
        print('myClass2' + b + ',' + x)


class MyClass1(LoggingBase):

    def print_some_thing(self, a):
        print('myClass1' + a)
        return MyClass2('test')     

'''

Simple version
with no class involved

'''    

  
def log(func, *args): 

    def inner_no_log():
        return func(*args)
    
    def inner_with_log():
        print('----- logging function name----' + str(func))
        for arg in args:
            print('parameter:' + arg)
        print('----- end logging parameter')
        rvalue = func(*args)
        print('-----log result:' + str(rvalue))
        return rvalue

    return inner_with_log() if islogging is True else inner_no_log()


def do_something_func(a, b):
    print('print:' + a + b)

    
def do_something_func2(a):
    print('print me' + a)
    
'''

simulated class version


'''


def obj_func(obj, a):
    print('func1' + str(obj) + a)

    
def obj_func2(obj, a, b):
    print('func2:' + a + ',' + b + ',' + str(obj))
    
    
def obj_func3(obj, a):
    print('func3' + +str(obj) + str(a))

    
def class_func(a):
    print('class func1: ' + a)


def init_func1(obj, a):
    obj['object data'] = {'a':a}
    

def init_func2(obj, a, b):
    obj['object data'] = {'a':a, 'b':b}

    
def create_class(class_name, init_func, obj_func_lst, class_func_lst):
    return {'class name':class_name, 'initialized function': init_func,
            'object functions':obj_func_lst, 'class function': class_func_lst}


class_objs = {'class1': create_class('class1', init_func1, {'obj_func':obj_func, 'obj_func2':obj_func2}, {}),
              'class2': create_class('class2', init_func2, {'obj_func3': obj_func3 },
                                               {'class_func': class_func})}


def invoke_object_method(obj, func_name, *args):
    return obj['object methods'][func_name](obj, * args)


def invoke_class_method(class_name, class_func_name, *args):
    return class_objs[class_name]['class function'][class_func_name](*args)


def create_obj_by_class(class_name, *args):
    new_obj = {}
    class_objs[class_name]['initialized function'](new_obj, *args)
    new_obj['object methods'] = class_objs[class_name]['object functions']
    new_obj['class function'] = class_objs[class_name]['class function']
    return new_obj
    
    
if __name__ == '__main__':
    MyClass1().print_some_thing('hello').print_me('world', '!')
    MyClass2('test2').a
    
    print('-----------------')
    
    log(do_something_func, 'hello', 'world')
    log(do_something_func2, 'world2')
    
    print('-------------------test my own class system')
    
    my_class1_obj = create_obj_by_class('class1', 'first class')

    invoke_object_method(my_class1_obj, 'obj_func2', 'hello', 'world')  
    invoke_class_method('class2', 'class_func', 'hello class ')
    
