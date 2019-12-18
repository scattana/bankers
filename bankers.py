# -*- coding: utf-8 -*-
"""
@author: scatt
"""

import csv

# utility function to add two lists element-by-element
def add_lists(l1, l2):
    temp = []
    for i in range(len(l1)):
        temp.append(l1[i]+l2[i])
    return temp

# utility function to determine whether existing state is sufficient for process execution
def is_suff_for_proc(hyp, need, req, p, held):
    for i in range(len(hyp)):
        if hyp[i] < need[i]:
            return False
    return True

# "greater than or equal to" operator for two lists (element-by-element)
def is_gte(l1, l2):
    for i in range(len(l1)):
        if l1[i] < l2[i]:
            return False
    return True

# "banker" function implements banker's algorithm and determines whether to grant or deny req
def banker(processes, proc, resources, req, held):
    # first, just check if there simply aren't enough remaining resources to complete the request
    for i in range(len(resources)):
        if resources[i] < req[i]:
            return False
    # even if there ARE enough resources, deny the request if granting would lead to deadlock
    # (b/c at least 1 remaining resource would be less than what's needed for 1 proc to complete)
    hyp_remaining = []
    for i in range(len(resources)):
        hyp_remaining.append(resources[i] - req[i])
    if add_lists(held[proc], req) == processes[proc]:
        hyp_remaining = add_lists(hyp_remaining, processes[proc])
    needed = {}
    for key in processes:
        needed[key] = []
        for i in range(len(resources)):
            needed[key].append(processes[key][i] - held[key][i])
    for key in processes:
        if is_suff_for_proc(hyp_remaining, needed[key], req, processes[key], held[key]):
            return True
    # edge case: request would complete the process in question
    if is_gte(add_lists(req, hyp_remaining), needed[proc]):
        return True
    return False


def main(file):
    source = []
    with open(file) as fd:
        rd = csv.reader(fd, delimiter='\t')
        for row in rd:
            source.append(row)
    
    # first row will always define existing resources
    resources = []
    for arg in source[0][1:]:
        resources.append(int(arg))
    
    # verbose output for resource definition
    x = ', '.join(str(r) for r in resources)
    print('existing resources are defined ('+x+')')
    
    # loop through commands and reject or grant resources as appropriate
    processes = {}
    held = {}
    for cmd in source[1:]:
        if cmd[0] == 'd':
            processes[cmd[1]] = [int(item) for item in cmd[2:]]
            x = ', '.join(str(num) for num in processes[cmd[1]])
            held[cmd[1]] = [0 for i in range(len(cmd[2:]))]
            print('process '+cmd[1]+' is defined with max ('+x+')')
        if cmd[0] == 'r':
            proc = cmd[1]
            req = [int(item) for item in cmd[2:]]
            x = ', '.join(str(num) for num in req)
            if not banker(processes, proc, resources, req, held):
                print('process '+proc+' requests ('+x+') -> rejected')
            else:
                for i in range(len(req)):
                    resources[i] -= req[i]
                    held[proc][i] += req[i]
                if processes[proc] == held[proc]:
                    for i in range(len(req)):
                        resources[i] += held[proc][i]
                    held.pop(proc)
                    processes.pop(proc)
                    print('process '+proc+' requests ('+x+') -> granted ... process '+proc+' is complete')
                else:
                    print('process '+proc+' requests ('+x+') -> granted')



if __name__ == "__main__":
    in_file = "input1.txt"              # SPECIFY THE INPUT FILE HERE
    main(in_file)