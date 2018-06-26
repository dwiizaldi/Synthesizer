#!/usr/bin/python

import sys
import time

# attribute
# delay=a,b,c,d
# a: POST forward-path delay
# b : POST backward-path delay
# c : GET forward-path delay
# d : GET backward-path delay

attr = '0,0,0,0'
delay_post_f = sys.argv[1]
delay_post_b = sys.argv[2]
delay_get_f = sys.argv[3]
delay_get_b = sys.argv[4]



file = open("delayattr.txt","w+")

def extract_delay_attributes(argv):
  global attr, delay_post_f, delay_post_b, delay_get_f, delay_get_b
  try:
        attr = argv.split('=')[1]
        delays = attr.split(',')
        try:
                delay_post_f = float(delays[0])
        except:
                delay_post_f = 0
        try:
                delay_post_b = float(delays[1])
        except:
                delay_post_b = 0
        try:
                delay_get_f = float(delays[2])
        except:
                delay_get_f = 0
        try:
                delay_get_b = float(delays[3])
        except:
                delay_get_b = 0
  except:
        pass


# ----------MAIN------------

try:
   extract_delay_attributes(sys.argv[3])
   
   time.sleep(delay_post_f)
   time.sleep(delay_post_b)
   time.sleep(delay_get_f)
   time.sleep(delay_get_b)


except:
   pass

file.write(delay_post_f +'\n'+ delay_post_b +'\n'+ delay_get_f +'\n'+ delay_get_b)
#file.write(delay_post_f + delay_post_b + delay_get_f + delay_get_b)
file.close()
print 'Delay: %s %s %s %s' % (delay_post_f, delay_post_b, delay_get_f, delay_get_b)
#print 'First delay'
#time.sleep(float(delay_post_f))
#print 'Second delay'
#time.sleep(float(delay_post_b))
#print 'Third delay'
#time.sleep(float(delay_get_f))
#print 'Last delay'
#time.sleep(float(delay_get_b))
#print 'This is the end'
