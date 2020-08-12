# -*- coding: utf-8 -*-
from RPi import GPIO
import config as cfg
import time

## Variable setting
# GPIO
sensor = 17 # 指尖传感器
switch = 18 # 开关
sensor_bounce_time = 200 # 开关触发时间
switch_bounce_time = 1000 # 开关触发时间

# K-test
full_test_num = 3 # 总共需要完成测试的数量
result_list = [] # 结果队列
test_num = 0     # 已完成测试数量
success_num = 0  # 成功数量
begin_flag = 0  # 开关按下标志
SUCCESS = 1
FAILED = 0

# 毫秒级时间戳
Get_time_stamp = lambda:int(round(time.time() * 1000))

print("*********************  Kapandji TEST BEGIN  *********************")

# GPIO config
cfg.Gpio_config(sensor, switch, sensor_bounce_time, switch_bounce_time)

 
#--------------------------------------------  main
try:
    while True:
        # begin_flag 0时按下开关开始计时
        if (not begin_flag and GPIO.event_detected(switch)):
            test_num = test_num + 1
            print('Begin singal kapandji test ----', test_num)
            begin_flag = 1
            t = Get_time_stamp()
            continue
        
        # begin_flag 1 时按下开关表示失败测试并开始下一次测试
        if (begin_flag and GPIO.event_detected(switch)):
            result_list, success_num = cfg.Record_test_result(FAILED, 0, test_num, success_num, result_list)
            begin_flag = 0
            t = Get_time_stamp()
            continue
            

        # begin_flag 1时按下传感器接触表明完成一次测试
        if (begin_flag and GPIO.event_detected(sensor)):
            delta_t = (Get_time_stamp() - t)/1000 #转化为秒
            result_list, success_num = cfg.Record_test_result(SUCCESS, delta_t, test_num, success_num, result_list)
            begin_flag = 0
            continue
            

        # 完成所有测试组
        if (not begin_flag and test_num == full_test_num):
            test_num, success_num, result_list = cfg.Record_all_test_result(test_num, success_num, result_list)
            continue
            
        # 可以在循环中做其他检测
        time.sleep(0.01)     # 10毫秒的检测间隔
except Exception as e:
    print(e)
 
# 清理占用的GPIO资源
GPIO.cleanup()