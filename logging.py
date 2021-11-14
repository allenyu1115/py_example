'''
Created on Nov 14, 2021

@author: Allen Yu
'''

class LoggingBase:
    def __getattribute__(self, item):
        attr = super(LoggingBase, self).__getattribute__(item)
        attr_type = type(attr)
        print(attr_type)
        def decorate_func(*args):
            print('class :' + str(self) + ';method:' + str(attr.__func__))
            for arg in args:
                print('parameter: ' + arg)
            rval= attr.__func__(self, *args)
            print('the result log:' + str(rval))
            return rval
        return decorate_func
    
class MyClass2(LoggingBase):
    def __init__(self,a):
        self.a = a
        
    def print_me(self,b, x):
        print('myClass2' + b + ',' + x)

class MyClass1(LoggingBase):
    def print_some_thing(self,a):
        print('myClass1' + a)
        return MyClass2('test')  
    
if __name__ == '__main__':
    MyClass1().print_some_thing('hello').print_me('world','!')
    MyClass2('test2').a