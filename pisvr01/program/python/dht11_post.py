import RPi.GPIO as GPIO
import commands
import os
import glob
import psutil
import time
import socket
import MySQLdb as mysql
import datetime

channel =4 

def get_temp():
	data = []
	j = 0

	GPIO.setmode(GPIO.BCM)

	time.sleep(1)

	GPIO.setup(channel, GPIO.OUT)
	GPIO.output(channel, GPIO.LOW)
	time.sleep(0.02)
	GPIO.output(channel, GPIO.HIGH)
	GPIO.setup(channel, GPIO.IN)

	while GPIO.input(channel) == GPIO.LOW:
	  continue
	while GPIO.input(channel) == GPIO.HIGH:
	  continue

	while j < 40:
	  k = 0
	  while GPIO.input(channel) == GPIO.LOW:
		continue
	  while GPIO.input(channel) == GPIO.HIGH:
		k += 1
		if k > 100:
		  break
	  if k < 8:
		data.append(0)
	  else:
		data.append(1)

	  j += 1

	#print "sensor is working."
	#print data

	humidity_bit = data[0:8]
	humidity_point_bit = data[8:16]
	temperature_bit = data[16:24]
	temperature_point_bit = data[24:32]
	check_bit = data[32:40]

	humidity = 0
	humidity_point = 0
	temperature = 0
	temperature_point = 0
	check = 0

	for i in range(8):
	  humidity += humidity_bit[i] * 2 ** (7-i)
	  humidity_point += humidity_point_bit[i] * 2 ** (7-i)
	  temperature += temperature_bit[i] * 2 ** (7-i)
	  temperature_point += temperature_point_bit[i] * 2 ** (7-i)
	  check += check_bit[i] * 2 ** (7-i)

	tmp = humidity + humidity_point + temperature + temperature_point
	return check,tmp,temperature,humidity

def get_correct_temp():
	CHECK, TMP, TEMP_C, HUMIDITY = get_temp()
	while CHECK != TMP:
           GPIO.cleanup()
           time.sleep(1)
	   CHECK, TMP, TEMP_C, HUMIDITY = get_temp()
	   
	TEMP_F = TEMP_C * 9.0 / 5.0 + 32.0   
	return TEMP_C, TEMP_F, str(HUMIDITY) +"%"

def get_cpu_temp():
 tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
 cpu_temp = tempFile.read()
 tempFile.close()
 return float(cpu_temp)/1000
 # Uncomment the next line if you want the temp in Fahrenheit
 #return float(1.8*cpu_temp)+32
 
def get_gpu_temp():
 gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
 return float(gpu_temp)
 # Uncomment the next line if you want the temp in Fahrenheit
 # return float(1.8* gpu_temp)+32

# Return RAM information (unit=kb) in a list  
# Index 0: total RAM  
# Index 1: used RAM 
# Index 2: free RAM 

def getRAMinfo():
 p =os.popen('free')
 i =0
 while 1:
     i =i +1
     line =p.readline()
     if i==2:
           return(line.split()[1:4])
		   
 

# Return % of CPU used by user as a character string  
def getCPUuse():
  return(str(psutil.cpu_percent(1))+"%")

 

# Return information about disk space as a list (unit included)  
# Index 0: total disk space  
# Index 1: used disk space  
# Index 2: remaining disk space  
# Index 3: percentage of disk used  

def getDiskSpace():
 p =os.popen("df -h /")
 i =0
 while 1:
      i =i +1
      line = p.readline()
      if i == 2:
             return(line.split()[1:5])
 
#post sensor data collection
def post_data():
	conn = mysql.connect(
		host = 'localhost',
		port = 3306,
		user = 'admin',
		passwd = 'Osram9809',
		db = 'myiot'
		)
	try:
		CPU_temp = get_cpu_temp()
		GPU_temp = get_gpu_temp()
		CPU_use = getCPUuse()
		ROOM_temp_c, ROOM_temp_f, ROOM_humidity = get_correct_temp()

# RAM information
# Output is in kb, here I convert it in Mb for readability
		RAM_stats = getRAMinfo()
		RAM_total = round(int(RAM_stats[0]) /1000,1)
		RAM_used = round(int(RAM_stats[1]) /1000,1)
		RAM_free = round(int(RAM_stats[2]) /1000,1)
  


# Disk information
		DISK_stats = getDiskSpace()
		DISK_total = DISK_stats[0]
		DISK_used = DISK_stats[1]
		DISK_perc = DISK_stats[3]
		HOST_name = socket.gethostname()  

		dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		y = datetime.datetime.now().strftime("%Y")

#Connect MySQL 
		conn = mysql.connect(
		host = 'localhost',
		port = 3306,
		user = 'admin',
		passwd = 'Osram9809',
		db = 'myiot'
		)

		cur = conn.cursor()
  #cur.execute("SELECT VERSION()")
  #version = cur.fetchone()
  #print(version)
		sql = """INSERT INTO tb_temperature (hostname, location, room_temp_c, room_temp_f, room_humidity, 
			cpu_temp, gpu_temp, cpu_use, ram_total, ram_used, ram_free, disk_total, disk_used, disk_used_perc,
			creation_year, creation_datetime
			) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"""
		cur.execute(sql,
			( HOST_name, 'DG1', ROOM_temp_c, ROOM_temp_f, ROOM_humidity,  
			CPU_temp, GPU_temp, CPU_use, RAM_total, RAM_used, RAM_free, DISK_total, DISK_used, DISK_perc, y, dt
			))
		conn.commit()
	except mysql.Error, e:
		print "Error %d:%s" % (e.args[0], e.args[1])
		exit(1)  
 
	finally:
		if conn:
			conn.close()
 
#while True:
# print(read_temp()) 
# time.sleep(1)

if __name__ == '__main__':
	post_data()

