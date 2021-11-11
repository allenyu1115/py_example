'''
@author: ayu
'''
    
from threading import Thread
import time

if __name__ == '__main__':

    def os(gui_display_simulator, event_handler_register):
        '''
        event handler register is how to handle event logic 
        '''
        event_list_buffer = []
        gui_display_data = []
        keyboard_input = []  
        
        def key_board(keyboard_input):
            while True:
                time.sleep(1)
                '''
                simulate key board generated event data , 1 is event type, 2 is event body data
                '''
                keyboard_input.append((1, 2))
    
        def gui(event_list_buffer, event_handler_register):
            while True:
                if len(event_list_buffer) != 0:
                    event = event_list_buffer.pop()
                    event_handler_func = event_handler_register.get(event[0])
                    if event_handler_func:
                        event_handler_func(event[1], gui_display_data)
                        gui_display_simulator(gui_display_data)
                time.sleep(1)
    
        gpu = Thread(target=gui, args=(event_list_buffer, event_handler_register))
        gpu.start()
        
        keyboard_compute_unit = Thread(target=key_board, args=(keyboard_input,))
        keyboard_compute_unit.start()
         
        while True:
            if len(keyboard_input) != 0:
                event = keyboard_input.pop()
                if event:
                    event_list_buffer.append(event)
            time.sleep(1)
    '''
    event type is 1 , how to handle event type 1, this handler just puts the event body into gui display data list
    '''
    os(lambda x:print(x), {1: lambda x, y: y.append(x) })
