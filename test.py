'''
compare the site_type_for_cc.txt

'''
from main import map_list,filter_list
import os
      
def read_from_file(file_path):
    with open(file_path) as f:
        return f.readlines()

if __name__ == '__main__':
    
    site_type_lst = read_from_file(os.path.join('files','site_type_for_cc.txt'))
    #remove \n 
    all_icon_lst = map_list(read_from_file(os.path.join('files','all_icons_name.txt')),lambda x: x.strip()[:-4]) 
    # map original list  remove space, remove \r\n, remove \ remove / .  add st_
    arranged_lst = map_list(filter_list(map_list(site_type_lst, lambda x : x.strip().replace(' ','').replace('\\','').replace('/','').lower()), 
                      lambda x: True if not x.startswith('-----------------') else False), lambda x: 'st_' + x)
    #filter 
    rlst = filter_list(arranged_lst, lambda x: True if x not in all_icon_lst else False)
    print(rlst)
    print(len(rlst))
    
    