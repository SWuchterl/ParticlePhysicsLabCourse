#!/usr/bin/python
import time

for iteration in ['first', 'second', 'third', 'fourth']:
    time.sleep(1)
    for i in range(1, 5):
        filename = iteration + '_iteration/efficiency_PMT' + str(i) + '.py'
        print '\n' + '************************************************************'
        print '\n' + 'executing ' + filename + '\n'
        execfile(filename)
