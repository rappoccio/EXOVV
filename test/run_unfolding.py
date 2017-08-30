#!/usr/bin/env python



from subprocess import call

call("python 2Dunfold_data.py " , shell=True)
call("python 2Dunfold_mc.py " , shell=True)

for exten in ["_nomnom","_jerup","_jerdn","_jernom","_jecup","_jecdn","_jmrnom","_jmrup","_jmrdn","_puup","_pudn","_jmsup","_jmsdn"] : 
    call("python 2Dunfold_data.py --extension " + exten , shell=True)
    call("python 2Dunfold_mc.py --extension " + exten , shell=True)



for i in xrange(53) : 

    call("python 2Dunfold_data.py --extension _jecsrc" + str(i) + "up" , shell=True)
    call("python 2Dunfold_data.py --extension _jecsrc" + str(i) + "dn" , shell=True)

    call("python 2Dunfold_mc.py --extension _jecsrc" + str(i) + "up" , shell=True)
    call("python 2Dunfold_mc.py --extension _jecsrc" + str(i) + "dn" , shell=True)
