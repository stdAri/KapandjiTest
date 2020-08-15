# -*- coding: utf-8 -*-
from RPi import GPIO
import config as cfg
import time

## Variable setting
# GPIO
sensor = 17 # 指尖传感器
switch = 18 # 开关
sensor_bounce_time = 400 # 开关触发时间
switch_bounce_time = 1000 # 开关触发时间

# K-test
full_test_num = 10 # 总共需要完成测试的数量
result_list = [] # 结果队列
test_num = 0     # 已完成测试数量
success_num = 0  # 成功数量
begin_flag = 0  # 开关按下标志
fail_time = 20 # 失败时间阈值
SUCCESS = 1
FAILED = 0

# 测试者姓
name = "zhang"

# 毫秒级时间戳
Get_time_stamp = lambda:int(round(time.time() * 1000))

print("*********************  Kapandji TEST BEGIN  *********************")
print("Full test num: ", full_test_num, "\nFail time: ", fail_time)
number = input("Input the No. of the test: ")

# GPIO config
cfg.Gpio_config(sensor, switch, sensor_bounce_time, switch_bounce_time)

 
#--------------------------------------------  main
try:
    while True: #总测试循环
        key = input()

        if (key == "" or key == " "): ##输入回车
            # 开始一组K-test
            test_num = cfg.Start_single_test(test_num)
            t = Get_time_stamp()
            time.sleep(0.1)     # 100毫秒的延迟，消除干扰
            
            while True: # 单次测试循环
                delta_t = (Get_time_stamp() - t ) / 1000

                # 大于fail_time认为失败
                if (delta_t > fail_time):
                    result_list, success_num = cfg.Record_test_result(FAILED, 0, test_num, success_num, result_list)
                    break
                
                # fail_time内锡纸接触认为成功
                if (GPIO.event_detected(sensor)):
                    if (GPIO.input(sensor) == GPIO.HIGH):
                        # print(GPIO.input(sensor))
                        result_list, success_num = cfg.Record_test_result(SUCCESS, delta_t, test_num, success_num, result_list)
                        break

        # 完成所有测试组
        if (not begin_flag and test_num == full_test_num):
            test_num, success_num, result_list = cfg.Record_all_test_result(name, number, test_num, success_num, result_list)
            number = input("Input the No. of the test: ")
            continue
                
        if (key == "q"):
            break
        # 可以在循环中做其他检测
        time.sleep(0.01)     # 10毫秒的检测间隔
except Exception as e:
    print(e)
 
# 清理占用的GPIO资源
GPIO.cleanup()