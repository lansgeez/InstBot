from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from date import users_settings_dict, hashtag, coms, skipword
import time
import random
import datetime
from random import randint

global writef

writef = datetime.datetime.now().strftime("%d-%m-%Y %H %M")
f = open(f'logs/{writef}.txt', 'w')
f.close()

class InstagramBot():

    def __init__(self, username, password, hashtag, coms, skipword):
        self.username = username
        self.password = password
        #options=webdriver.ChromeOptions()
        #options.add_argument("--headless")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # метод для закрытия браузера
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):

        global writef, nextacc
        nextacc = 0
        now = datetime.datetime.now()
        f = open(f'logs/{writef}.txt', 'a')
        f.write("--------------------------------\n")
        f.write("Аккаунт - "+ username + "\n")
        f.write("Сессия от " + now.strftime("%d-%m-%Y %H:%M") + "\n")
        
        f.close()

        browser = self.browser
        
        browser.get('https://www.instagram.com')

        time.sleep(random.randrange(2, 3)) #задержка перед вводом логина
        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(random.randrange(2, 3)) #задержка перед вводом пароля
        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)
        print("--------------------------------")
        print("Аккаунт - "+ username)
        print("Сессия от "+now.strftime("%d-%m-%Y %H:%M"))
        print("--------------------------------")
        password_input.send_keys(Keys.ENTER)
        time.sleep(10) #задержка после входа в аккаунт
        global comotl,allcount,progon
        comotl = 0
        allcount = 0
        progon = 0

    def sessionacccomplited(self):
        print("--------------------------------")
        print("Сессия аккаунта - " +username + ". завершена в - " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        print("--------------------------------")
        print("\n")
        f = open(f'logs/{writef}.txt', 'a')
        f.write("--------------------------------\n")
        f.write("Сессия аккаунта - " +username + ". завершена в - " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + "\n")
        f.write("--------------------------------\n")
        f.close()

    # метод ставит лайки и отправляет коменты по 6-ти хештегам
    def like_photo_by_hashtag(self):
    
        global comotl,allcount, writef,progon, nextacc
        if progon == len(hashtag):
            progon = 0
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag[progon]}/')
        
        print('Поиск по хештегу - ', hashtag[progon])

        f = open(f'logs/{writef}.txt', 'a')
        f.write("--------------------------------")
        f.write("\n")
        f.write("Поиск по хештегу - " + hashtag[progon])
        f.write("\n")
        f.write("--------------------------------")
        f.write("\n")
        f.close()
        time.sleep(5) #задержка перехода на хештег
        count = 0
        #открывает 10 пост
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()

        #в хештеге обрабатывает 40 постов
        for i in range(39):
            if allcount == 100:
                nextacc = 1
                break
            if comotl == 1:
                nextacc = 1
                break
			
            try:
                #перелистывает пост на 1
                browser.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()

                #для того, чтобы не коментил посты которые уже пройдены
                likes = 1

                #лайкаем если нашли лайк  
                liketry = 0

                time.sleep(random.randrange(3, 4))
                #если это видео то все ок
                if browser.find_element_by_class_name('fXIG0') :
                    try:
                        names = browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a')
                        teg = 0
                        href = names.get_attribute('href')
                        for i in range(len(skipword)):
                            if skipword[i] in href and teg == 0:
                                print("--------------------------------")
                                print(skipword[i])
                                print("Конкурент - ", href)
                                print("--------------------------------")
                                teg = 1
                    except Exception as ex:
                        print(ex)

                    #лайкинг
                    try:
                        #проверка не пройден ли пост
                        testlike = browser.find_elements_by_tag_name('svg')
                        for itemq in testlike:
                            href = itemq.get_attribute('width')
                            if href == '24':
                                href = itemq.get_attribute('aria-label')
                                if href == 'Нравится' and teg == 0:
                                    liketry = 1
                    except Exception as ex:
                        print(ex)
                        print('Ошибка. В попытке проверки не пройден ли пост')

                    try:
                        if liketry == 1:
                            # задержка перед лайком поста
                            time.sleep(random.randrange(2, 3))
                            allcount += 1
                            browser.find_element_by_xpath(
                                        '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
                            print(allcount, '- лайк поставлен')
                            f = open(f'logs/{writef}.txt', 'a')
                            f.write(str(allcount))
                            f.write(" - лайк отправлен")
                            f.write("\n")
                            f.close()
                            # задержка после лайка
                            time.sleep(random.randrange(2, 3))
                            # для того, чтобы не коментил посты которые уже пройдены
                            likes = 0
                        
                    except Exception as ex:
                        print(ex)
                        print('Ошибка. В попытке поставить лайк')
                    
                    #комментирование
                    try:
                        #если коменты не отлетели то ставим коммент и пост не пройден
                        if comotl == 0 and likes == 0:
                            #задержка перед коментом
                            time.sleep(random.randrange(26, 36))
                            comment = browser.find_element_by_class_name('Ypffh')
                            comment.click()
                            comment = browser.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                            indexcom = randint(0, 4)
                            #пишем комментарий
                            comment.send_keys(coms[indexcom])
                            time.sleep(1)
                            #отправляем комментарий
                            comment.send_keys(Keys.ENTER)
                            print(allcount, '- коммент поставлен')
                            time.sleep(random.randrange(4,6))
                            f = open(f'logs/{writef}.txt', 'a')
                            f.write(str(allcount))
                            f.write(" - коммент отправлен")
                            f.write("\n")
                            f.close()
                            
                    except Exception as ex:
                        print(ex)
                        print('Ошибка. В попытке отправления комментария')

                if likes == 1 and teg == 0:
                    print('--------------------------------')
                    print('Пост пройден')
                    print('--------------------------------')

            except Exception as ex:
                print(ex)
        progon += 1


global progon, nextacc
ifinished = 0
for user,user_data in users_settings_dict.items():
    username=user_data['login']
    password=user_data['password']
        
    instbot = InstagramBot(username, password, hashtag, coms, skipword)
    
    instbot.login()
    
    while nextacc == 0:
        instbot.like_photo_by_hashtag()
        
    instbot.sessionacccomplited()
        
    ifinished += 1
    if ifinished == len(users_settings_dict.items()):
        instbot.close_browser()
    else:
        instbot.close_browser()
        time.sleep(240)
    
    
