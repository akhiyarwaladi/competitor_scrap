# Android environment
import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
# from appium.webdriver.common.touch_action import TouchAction
from time import sleep
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
import pandas as pd
import random
import os

desired_caps = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='emulator-5554',
    appPackage="com.astro.shop",
    appActivity='.MainActivity',
    newCommandTimeout=3000,
    noReset=True
)

cat_list = [
"Netizen's Favorites",
" Vitamin",
"Ibu & Bayi",
"Bahan Masak & Bumbu",
"Susu & Olahan Susu",
"Kebutuhan Pokok",
"Tepung & Bahan Kue",
"Minuman"
]

while(True):
    for cat_name in cat_list:
        # cat_name = cat_list[2]
        spath = './res/_{}_.xlsx'.format(cat_name)
        if os.path.exists(spath):
            continue

        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        sleep((random.randint(1, 5)))
        


        while(True):
            try:
               
                el = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"{}\")".format(cat_name))
                print(el)
            


                break
            except Exception as e:

                actions = ActionChains(driver)
                # override as 'touch' pointer action
                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location((random.randint(200, 400)), 950)
                actions.w3c_actions.pointer_action.pointer_down()
                # actions.w3c_actions.pointer_action.pause(2)
                actions.w3c_actions.pointer_action.move_to_location((random.randint(200, 400)), 400)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                # TouchAction(driver).press(x=220, y=800).move_to(x=220, y=400).release().perform()
                sleep((random.randint(5, 10)))
                ele = driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
                for e in ele:
                    print(e.text)


        el.click()


        sleep(2)



        # finger = 0
        # actions = ActionChains(driver)
        # actions.w3c_actions.devices = []


        # finger += 1
        # x = 186
        # y = 712

        # # https://github.com/SeleniumHQ/selenium/blob/64447d4b03f6986337d1ca8d8b6476653570bcc1/py/selenium/webdriver/common/actions/pointer_input.py#L24
        # new_input = actions.w3c_actions.add_pointer_input('touch', f'finger{finger}')
        # new_input.create_pointer_move(x=x, y=y)
        # new_input.create_pointer_down(MouseButton.LEFT)
        # new_input.create_pause(0.1)
        # new_input.create_pointer_up(MouseButton.LEFT)
        # actions.perform()


        all_res = []
        init_text = ''
        while True:
            try:
                el = driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
                li_text = ''
                for e in el:
                    print(e.text)
                    li_text = li_text+e.text+'\n'

                if li_text == init_text:
                    print('finished scroll')
                    all_res = pd.concat(all_res)
                    all_res = all_res.drop_duplicates(['product','price'])

                    

                    adder = 'sheet1'
                    writer = pd.ExcelWriter(spath, engine='xlsxwriter') 
                    all_res.to_excel(writer, sheet_name=adder, index=False)

                    # Auto-adjust columns' width
                    for column in all_res:
                        column_width = max(all_res[column].astype(str).map(len).max(), len(column))
                        col_idx = all_res.columns.get_loc(column)
                        writer.sheets[adder].set_column(col_idx, col_idx, column_width)

                    writer.save()
                    break

                li_price=[]
                li_product=[]

                li_el = li_text.split('\n')
                for idx,el in enumerate(li_el):
                    print(li_el[idx])
                    if li_el[idx].startswith('Rp'):
                        if li_el[idx+1].startswith('Rp') or li_el[idx+1].startswith('1'):
                            continue
                        li_price.append(li_el[idx])
                        li_product.append(li_el[idx+1])
                        
                res = pd.DataFrame({'product':li_product,'price':li_price})
                all_res.append(res)
                print(res)
                if len(res) <= 0:
                    break


                init_text = li_text
                actions = ActionChains(driver)
                # override as 'touch' pointer action
                actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location((random.randint(200, 400)), 950)
                actions.w3c_actions.pointer_action.pointer_down()
                # actions.w3c_actions.pointer_action.pause(2)
                actions.w3c_actions.pointer_action.move_to_location((random.randint(200, 400)), 400)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                
                # TouchAction(driver).press(x=220, y=800).move_to(x=220, y=400).release().perform()
                sleep((random.randint(8, 10)))

                #break

            except Exception as e:
                print(e)
                break



        #driver.back()
        driver.close_app()
        sleep((random.randint(1, 3)))



    '''
    {
    "platformName":"Android",
    "appium:deviceName": "emulator-5554",
    "appium:appPackage": "com.astro.shop",
    "appium:appActivity": ".MainActivity",
    "platformName": "Android",
    "appium:automationName": "uiautomator2",
    "appium:noReset": true
    }
    '''