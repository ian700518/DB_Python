#!/usr/bin/python3

import logging
from subproc import Send_Command

GPIOCTRL_0 = 0x10000600
GPIOCTRL_1 = 0x10000604
GPIOCTRL_2 = 0x10000608

GPIODATA_0 = 0x10000620
GPIODATA_1 = 0x10000624
GPIODATA_2 = 0x10000628

GPIO_SWBTN_NUM = 0
GPIO_WAKEUP_NUM = 2
GPIO_RESET_NUM = 3
GPIO_P04_NUM = 45
GPIO_P15_NUM = 1
GPIO_P20_NUM = 46
GPIO_P24_NUM = 6
GPIO_EAN_NUM = 11
GPIO_USB1PWR_NUM = 4
GPIO_USB2PWR_NUM = 5
GPIO_WCEN_NUM = 18
GPIO_WCRDY_NUM = 19

DIRECT_OUT = 1
DIRECT_IN = 0

logger_gpio = logging.getLogger('GPIO_LOG')

def PinInitial() :
    if GpioInitial(GPIO_USB1PWR_NUM, DIRECT_OUT, 1) != 1 :
        logging.error('GPIO_USB1PWR_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_USB2PWR_NUM, DIRECT_OUT, 1) != 1 :
        logging.error('GPIO_USB2PWR_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_WCEN_NUM, DIRECT_OUT, 1) != 1 :
        logging.error('GPIO_WCEN_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_WCRDY_NUM, DIRECT_IN, 0) != 1 :
        logging.error('GPIO_WCRDY_NUM Initialization faild~~~!!!')

    if GpioInitial(GPIO_SWBTN_NUM, DIRECT_OUT, 0) != 1 :
        logging.error('GPIO_SWBTN_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_WAKEUP_NUM, DIRECT_OUT, 0) != 1 :
        logging.error('GPIO_WAKEUP_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_RESET_NUM, DIRECT_OUT, 0) != 1 :
        logging.error('GPIO_RESET_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_P20_NUM, DIRECT_OUT, 0) != 1 :
        logging.error('GPIO_P20_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_P24_NUM, DIRECT_OUT, 0) != 1 :
        logging.error('GPIO_P24_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_EAN_NUM, DIRECT_OUT, 0) != 1 :
        logging.error('GPIO_EAN_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_P04_NUM, DIRECT_IN, 0) != 1 :
        logging.error('GPIO_P04_NUM Initialization faild~~~!!!')
    if GpioInitial(GPIO_P15_NUM, DIRECT_IN, 0) != 1 :
        logging.error('GPIO_P15_NUM Initialization faild~~~!!!')

def GetGpio(gpio_num) :
    logger_gpio.info('into get gpio function~~!!')
    gpio_div = int(gpio_num / 32)
    gpio_mod = gpio_num % 32
    if gpio_div == 0 :
        reg_add = GPIODATA_0
    elif gpio_div == 1 :
        reg_add = GPIODATA_1
    elif gpio_div == 2 :
        reg_add = GPIODATA_2
    else :
        logger_gpio.error('Gpio Number Error~~!!!')
    command = 'devmem 0x{:08x}'.format(reg_add)
    logger_gpio.debug('GetGpio command = {}'.format(command))
    original_val = int(Send_Command(command), 16)
    logger_gpio.debug('at GetGpio original_val = 0x{:08x}'.format(original_val))
    original_val ^= (1 << gpio_mod)
    if original_val == 0 :
        return 1
    else :
        return 0


def SetGpio(gpio_num, val) :
    logger_gpio.info('into set gpio function~~!!')
    gpio_div = int(gpio_num / 32)
    gpio_mod = gpio_num % 32
    if gpio_div == 0 :
        reg_add = GPIODATA_0
    elif gpio_div == 1 :
        reg_add = GPIODATA_1
    elif gpio_div == 2 :
        reg_add = GPIODATA_2
    else :
        logger_gpio.error('Gpio Number Error~~!!!')
        return -1

    command = 'devmem 0x{:08x}'.format(reg_add)
    logger_gpio.debug('SetGpio command = {}'.format(command))
    original_val = int(Send_Command(command), 16)
    logger_gpio.debug('original_val = 0x{:08x}'.format(original_val))
    if val == 1 :
        original_val |= (val << gpio_mod)
    else :
        original_val &= ~(1 << gpio_mod)
    command = 'devmem 0x{:08x} 32 0x{:08x}'.format(reg_add, original_val)
    logger_gpio.debug('SetGpio command = {}'.format(command))
    Send_Command(command)

def GpioInitial(gpio_num, mode, val) :
    logger_gpio.info('into Gpio Initialization~~!!')
    gpio_div = int(gpio_num / 32)
    gpio_mod = gpio_num % 32

#    logger_gpio.info('gpio_num is {},gpio_div is {}, gpio_mod is {}'.format(gpio_num, gpio_div, gpio_mod))
    if gpio_div == 0 :
        reg_add = GPIOCTRL_0
    elif gpio_div == 1 :
        reg_add = GPIOCTRL_1
    elif gpio_div == 2 :
        reg_add = GPIOCTRL_2
    else :
        logger_gpio.error('Gpio Number Error~~!!!')
        return -1

    command = 'devmem 0x{:08x}'.format(reg_add)
    original_val = int(Send_Command(command), 16)
    logger_gpio.debug('mode original_val = 0x{:08x}'.format(original_val))
    if mode == 1 :
        original_val |= (1 << gpio_mod)
    else :
        original_val &= ~(1 << gpio_mod)
    logger_gpio.debug('mode setting_val = 0x{:08x}'.format(original_val))
    command = 'devmem 0x{:08x} 32 0x{:08x}'.format(reg_add, original_val)
    logger_gpio.debug('GpioInitial command = {}'.format(command))
    Send_Command(command)
    command = 'devmem 0x{:08x}'.format(reg_add)
    change_val = int(Send_Command(command), 16)
    if (original_val & (1 << gpio_mod)) != (change_val & (1 << gpio_mod)) :
        logger_gpio.error('Mode setting faild~~!!!!')
        return -1

    if mode == 1 :
        if gpio_div == 0 :
            reg_add = GPIODATA_0
        elif gpio_div == 1 :
            reg_add = GPIODATA_1
        elif gpio_div == 2 :
            reg_add = GPIODATA_2
        else :
            logger_gpio.error('Gpio Number Error~~!!!')
            return -1

        command = 'devmem 0x{:08x}'.format(reg_add)
        original_val = int(Send_Command(command), 16)
        logger_gpio.debug('GpioInitial Get Pin val = 0x{:08x}'.format(original_val))
        if val == 1 :
            original_val |= (1 << gpio_mod)
        else :
            original_val &= ~(1 << gpio_mod)
        logger_gpio.debug('GpioInitial setting Pin val = 0x{:08x}'.format(original_val))
        command = 'devmem 0x{:08x} 32 0x{:08x}'.format(reg_add, original_val)
        logger_gpio.debug('GpioInitial Set Pin Val command = {}'.format(command))
        Send_Command(command)
        command = 'devmem 0x{:08x}'.format(reg_add)
        change_val = int(Send_Command(command), 16)
        if (original_val & (1 << gpio_mod)) != (change_val & (1 << gpio_mod)) :
            logger_gpio.error('Pin Val setting faild~~~!!!')
            return -1

    return 1
