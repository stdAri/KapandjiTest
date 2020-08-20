from RPi import GPIO
import time
import numpy as np
from pygame import mixer


SAVEFILE = 1

# raspi GPIO config 
def Gpio_config(sensor, switch, sensor_bounce_time, switch_bounce_time):
    # 采用BCM引脚编号
    GPIO.setmode(GPIO.BCM)
    # 关闭警告
    GPIO.setwarnings(True)

    # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
    GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    # 检测LOW -> HIGH的变化
    GPIO.add_event_detect(sensor, GPIO.RISING, bouncetime = sensor_bounce_time)
    GPIO.add_event_detect(switch, GPIO.RISING, bouncetime = switch_bounce_time)

def Start_single_test(test_num):
    test_num = test_num + 1
    print('Begin singal kapandji test ----', test_num)
    return test_num

# record test result
def Record_test_result(result, delta_time, test_num, success_num, result_list):
    print('Finish singal kapandji test ----', test_num)
    print(delta_time)
    result_list.append(delta_time)
    if result:
        success_num = success_num + 1
    return result_list,success_num

# record all test result and save to file  
def Record_all_test_result(name, number, test_num, success_num, result_list):
    # get timestamp filename
    filename = time.strftime('data/%Y-%m-%d %H:%M ',time.localtime()) + name + ' test ' + number + ".txt"
    result_list.append(round(sum(result_list)/success_num, 5))

    # print all result
    print("\n All result: ", result_list)
    print("\n Successful test number: ", success_num)
    print("\n Successful result mean: ",  result_list[test_num])

    # save all result
    if (SAVEFILE):
        np.savetxt(filename,np.array(result_list))

    # reset variable
    result_list = []
    test_num = 0
    success_num = 0
    
    return test_num, success_num, result_list

def play_sound(name, delay = 0):
    sound_dir_path = 'sound/'
    mixer.music.load(sound_dir_path + name)
    mixer.music.play()
    if (delay!=0):
        time.sleep(delay)
        mixer.music.stop()