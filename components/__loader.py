#!/usr/bin/env python3
import os

# ===Function: my_str===
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/components')
from sim_components import *

def MyStr(obj):
    """A quick dump of any object

    A function to dynamically create a '__str__' function in which all non-methods (non-callables)
    is turned into a string and returned to calling object. Probably could be cleaner but not
    interested right now in improving it.

    Args:
        None

    Returns:
        string: Representation of class

    """

    names = []
    vals = []
    for value in dir(obj):
        if not value.startswith('__') and not callable(obj.__getattribute__(value)):
            vals.append(obj.__getattribute__(value))
            names.append(value)
    string = "["+obj.__class__.__name__ + ":\n    ["
    for name in names:
        string += str(name) + ': %s, \n     '
    string = string[:-2]
    string += " ]\n]"
    return string % tuple(vals)

# ===Function: ProcessLoader===

class ProcessLoader(object):
    def __init__(self,input_file=None):
        if input_file is None:
            raise Exception("input file needed")

        self.jobs = []
        self.__apriori_file_processing(input_file)

    def get_jobs_list(self):
        return self.jobs

    def __apriori_file_processing(self,file_name):
        """
        Read the process data from given file name.
        Data format:
            Event   Time    Job     Memory  Run-Time
            ----    ----    ---     ------  --------
            A       131     5       513     64
            D       361

            Event   Time    IO-Burst-Time
            -----   ----    -------------
            I       214     85

            Event   Time    Semaphore
            -----   ----    ---------
            S       7183    2
            W       7287    3

            A = new process enters system
            D = Display status of simulator
            I = Process currently on cpu performs I/O
            S = Semaphore signal (release)
            W = Semaphore wait (acquire)
        """
        with open(file_name, 'r') as f:
            data = f.read()
        data = data.split('\n')
        for j in data:
            j = j.split()
            self.jobs.append(self.__build_dict(j))
                
    def get_process_list(self):
        processes = []

        # Create a list of actual processes with each of the data dictionaries
        for d in self.jobs:
            # The **d turns the dictionary into a list of keyword arguments
            # {'event': 'A', 'time': '100', 'runTime': '78', 'pid': '1', 'memory': '20'}
            # turns into:
            # event='A', time='100', runTime='78', pid=1, memory='20' 
            processes.append(Process(**d))
        return processes


    def __build_dict(self,vals):
        """
        Builds a kwargs dict for a new process initialization.
        """
        labels_dict = {}
        labels_dict['A'] = ['event', 'time', 'pid', 'mem_required', 'burst_time']
        labels_dict['I'] = ['event', 'time', 'ioBurstTime']
        labels_dict['W'] = ['event', 'time', 'semaphore']
        labels_dict['S'] = ['event', 'time', 'semaphore']
        labels_dict['D'] = ['event', 'time']    
        process_dict = {}
        labels = labels_dict[vals[0]]
        for i, item in enumerate(vals):
            process_dict[labels[i]] = vals[i].strip()
        return process_dict

    def __str__(self):
        return my_str(self)

def test_class_processLoader():
    test = ProcessLoader(os.path.dirname(os.path.realpath(__file__))+'/../input_data/cpu_sim_input.txt')
    p = test.get_jobs_list()
    print(p)

if __name__=='__main__':
    test_class_processLoader()