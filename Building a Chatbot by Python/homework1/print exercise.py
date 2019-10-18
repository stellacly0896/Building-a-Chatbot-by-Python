# Homework 1
# Author: Linyi Chen


def print_array( name, a ):
# 2 credits
    """ Print an array in a nice format.
    For instance, if name is "Vector x", the input array is [1,2,3]
    The function will print:
        Vector x: 1, 2, 3.
    """
    a_new = [str(i) for i in a]
    string = ",".join(a_new)
    print(name + " : " + string)


    # TODO fill the function. 2 credits



def print_process( current_step, total_step ):
# 2 credits
    """
    Print a process bar
    The current_step and total_step are both integers, where current_step <= total_step, and
    current_step is always non-negative.

    The line will be flushed, and it will be replaced by the next line.

    The process bar should have the format of 
    "             0.0%"
    "             7.8%"
    "#           10.2%"
    "###         39.8%"
    "########## 100.0%"
    Note: it will always contain 17 characters

    Each "#" sign represent 10%, and we always take the floor. (e.g. 11% and 19% both have only one "#" sign
    """

    # TODO  fill the function. 2 credits
    percentage = round(current_step * 100 / total_step, 1)
    well_num = int(current_step / total_step * 10)
    space_num = 17 - well_num - len(str(percentage)) - 1
    print("\r%s%s%s%%" % ("#" * well_num, " " *space_num, percentage), end ="")
    
#### Test Cases
    
print_array( "Small Primes", [2, 3, 5, 7, 11, 13, 17, 19 ])

print("12345678901234567890") # ruler
import time, random
total_s = 1024
current_s = 0

random.seed(0)
while True:
    print_process( current_s, total_s )
    time.sleep(0.1)
    if current_s >= total_s: break
    current_s += random.randint(0,50)
    current_s = min( current_s, total_s )

print()
print("Process done!")


""" The output of this program will be:


Small Primes: 2, 3, 5, 7, 11, 13, 17, 19.
12345678901234567890
########## 100.0%
Process done!


"""
