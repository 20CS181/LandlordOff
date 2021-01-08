"""
just used for debugging"""
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy

dict1 =  {'user':'old_child','num':[1,2,3]}
dict2 = dict1          # 浅拷贝: 引用对象
dict3 = dict1.copy()   # 浅拷贝：深拷贝父对象（一级目录），子对象（二级目录）不拷贝，还是引用
dict4 = copy.deepcopy(dict1)

# 修改 data 数据
dict1['user']='new_child'
dict1['num'].remove(1)

# 输出结果
print(dict1)
print(dict2)
print(dict3)
print(dict4)