#AUTHOR: yangxb
#CREATER: 2015-07-03 09:59:25
#FILENAME: Scan_file.py
#DESCRIPTION: 
#===============================================================
import os
import re
import json
def scan_file(jsonstring):
    try:
        arg_dict=json.loads(jsonstring)
        if arg_dict.has_key('path_list') and arg_dict.has_key('exclude'):
            if isinstance(arg_dict['path_list'], list) and isinstance(arg_dict['exclude'], unicode):
                path_list=arg_dict['path_list']
                exclude=arg_dict['exclude']
                re_dict={}
                if len(exclude) > 1:
                    for path in path_list:
                        _FILE_=[]
                        path=path.rstrip('/')
                        for  root,dirs,files in os.walk(path):
                                for filename in files:
                                        path_all=os.path.join(root,filename)
                                        p = re.search(exclude,path_all)
                                        if not p:
                                                _FILE_.append(os.path.join(root, filename))
                        re_dict[path]=_FILE_
                    return json.dumps(re_dict)
                else:
                    for path in path_list:
                        _FILE_=[]
                        path=path.rstrip('/')
                        for  root,dirs,files in os.walk(path):
                                for filename in files:
                                        _FILE_.append(os.path.join(root,filename))
                        re_dict[path]=_FILE_
                    return json.dumps(re_dict)

            else:return -5001
        else:return -5002
    except ValueError:
        return -5000
