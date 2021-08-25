from plugins import workFiles
from plugins import auth
import os
import vk_api
import random
from PIL import Image, ImageDraw, ImageFont
from vk_api.longpoll import  VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

get_data = workFiles.loadjson("config.json")
CardSetting = workFiles.loadjson("CardSetting.json")
token = str(get_data['token'])
users_dir = os.path.join(r"users/")

vk_session = vk_api.VkApi(token= token)
vk = vk_session.get_api()
longPool = VkLongPoll(vk_session)

ROOM = []

Профессия_базовая = str(CardSetting["Профессия_базовая"]).split(";")
Фобия_базовая = str(CardSetting["Фобия_базовая"]).split(";")
Болезнь_базовая = str(CardSetting["Болезнь_базовая"]).split(";")
Болезнь_стадия_базовая = str(CardSetting["Болезнь_стадия_базовая"]).split(";")
Телосложение_базовая = str(CardSetting["Телосложение_базовая"]).split(";")
Человеческая_черта_базовая = str(CardSetting["Человеческая_черта_базовая"]).split(";")
Хобби_базовая = str(CardSetting["Хобби_базовая"]).split(";")
Багаж_базовая = str(CardSetting["Багаж_базовая"]).split(";")
ДопИнф_базовая = str(CardSetting["ДопИнф_базовая"]).split(";")
Карта1_базовая = str(CardSetting["Карта1_базовая"]).split(";")
Карта2_базовая = str(CardSetting["Карта2_базовая"]).split(";")
Пол_базовая = str(CardSetting["Пол_базовая"]).split(";")
Плодовитость_базовая = str(CardSetting["Плодовитость_базовая"]).split(";")
РодственныеСвязи_базовая = str(CardSetting["РодственныеСвязи_базовая"]).split(";")

Котострофы_базовая = str(CardSetting["Котострофы_базовая"]).split(";")
Местанахождение_базовая = str(CardSetting["Местанахождение_базовая"]).split(";")
Комнаты_базовая = str(CardSetting["Комнаты_базовая"]).split(";")
ПредметыБункера_базовая = str(CardSetting["ПредметыБункера_базовая"]).split(";")
Дебафы_базовая = str(CardSetting["Дебафы_базовая"]).split(";")
КартаХода_базовая = str(CardSetting["КартаХода_базовая"]).split(";")
Прогноз_базовая = str(CardSetting["Прогноз_базовая"]).split(";")

def doc(user_id, doc_name, kb = ""):
    #doc = open("card.txt", "r")

    #a = vk.docs.getMessagesUploadServer(type = "doc", peer_id = user_id)
    #b = requests.post(a["upload_url"], files = {"file": doc}).json()
    #c = vk.docs.save(file = b["file"], title = doc_name)
    #d = 'doc{}_{}'.format(c["doc"]["owner_id"], c["doc"]["id"])

    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('card.jpg')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'

    if kb == "":
        vk.messages.send(user_id = user_id, attachment = attachment, random_id = 0)
    else:
        vk.messages.send(user_id = user_id, attachment = attachment, keyboard = kb, random_id = 0)

def set_status_userData(USER_Date, status):
    USER_Date["Status"] = status
    auth.saveUserData(id, USER_Date)

    return USER_Date

def set_Room_id_userData(USER_Date, Room_id):
    USER_Date["Room_id"] = Room_id
    auth.saveUserData(id, USER_Date)

    return USER_Date

def set_balance_userData(USER_Date, balance):
    USER_Date["balance"] = balance
    auth.saveUserData(id, USER_Date)

    return USER_Date

class GameRom():
    def __init__(self, host_id, room_id, user):
        self.host_id = host_id
        self.room_id = room_id
        self.user = user

        self.initCard()

        self.card_count = 1

    def setUser(self, user):
        self.user = user

    def initCard(self):
        self.Профессии = Профессия_базовая.copy()
        self.Фобии = Фобия_базовая.copy()
        self.Болезнь = Болезнь_базовая.copy()
        self.Болезнь_стадия = Болезнь_стадия_базовая.copy()
        self.Телосложение = Телосложение_базовая.copy()
        self.Человеческая_черта = Человеческая_черта_базовая.copy()
        self.Хобби = Хобби_базовая.copy()
        self.Багаж = Багаж_базовая.copy()
        self.ДопИнф = ДопИнф_базовая.copy()
        self.Карта1 = Карта1_базовая.copy()
        self.Карта2 = Карта2_базовая.copy()
        self.Пол = Пол_базовая.copy()
        self.Плодовитость = Плодовитость_базовая.copy()
        self.РодственныеСвязи = РодственныеСвязи_базовая.copy()

        self.RodSvaz = []

        self.КартыХода = КартаХода_базовая.copy()
        self.Котострофы = Котострофы_базовая.copy()
        self.Местанахождение = Местанахождение_базовая.copy()
        self.Комнаты = Комнаты_базовая.copy()
        self.ПредметыБункера = ПредметыБункера_базовая.copy()
        self.Дебафы = Дебафы_базовая.copy()
        self.Прогноз = Прогноз_базовая.copy()
        self.ТекущийПрогноз = "В этой игре случится следующее: " + self.Прогноз.pop(random.randint(0, len(self.Прогноз) - 1))
        self.БункерКатастрофа = "Катастрофа: " + self.Котострофы.pop(random.randint(0, len(self.Котострофы) - 1))
        self.БункерМестанахождение = "Ваш бункер находится в/под: " + self.Местанахождение.pop(
            random.randint(0, len(self.Местанахождение) - 1))
        self.БункерРазмер = random.randint(0, 1000)
        Комнат = 0
        self.БункерКомнаты = "В бункере есть спец. комнаты: "
        if self.БункерРазмер > 99:
            for i in range(100, self.БункерРазмер, 100):
                if Комнат < 5:
                    self.БункерКомнаты = self.БункерКомнаты + self.Комнаты.pop(random.randint(0, len(self.Комнаты) - 1)) + ", "
                    if Комнат == 1:
                        self.БункерКомнаты = self.БункерКомнаты + "\n"
                    Комнат = Комнат + 1

        self.БункерПредметы = "Также в вашем бункере повезло найти: " + self.ПредметыБункера.pop(
            random.randint(0, len(self.ПредметыБункера) - 1))
        self.БункерДебафы = "Но к сожалению в вашем бункере есть: " + self.Дебафы.pop(random.randint(0, len(self.Дебафы) - 1))
        self.БункерРазрушаемость = "И его разрушенность: " + str(random.randint(0, 40)) + "%"
        self.БункерВремя = "В этом бункере вам нужно пробыть " + str(random.randint(0,
                                                                               30)) + " лет. В бункере есть пища строго на этот период для 4 людей.\nКогда вы выйдете из бункера на земле можно будет относительно безопасно жить.\n" + self.ТекущийПрогноз

    def appendUser(self, id):
        self.user.append(id)

    def lenUser(self):
        return len(self.user)

    def remUser(self, id):
        self.user.remove(id)
        for i in self.user:
            sender(i, "Другой игрок вышел из комнаты")

    def testUser(self, id):
        testing = False
        for i in self.user:
            if id == i:
                testing = True
        return  testing

    def resetProf(self):
        for id in self.user:
            sender(id, 'Ваша новая профессия: ' + self.Профессии.pop(random.randint(0, len(self.Профессии) - 1)),
                   get_keyboard("войти в комнату"))

    def GetCardStep(self):
        tekCardHod = self.КартыХода.pop(random.randint(0, len(self.КартыХода) - 1))
        for id in self.user:
            sender(id, 'На этом ходу кое что случилось: ' + tekCardHod,
                   get_keyboard("войти в комнату"))

    def create_card(self, id):

        old = random.randint(1, 80)
        if old < 18:
            old = 18
        stash = str(random.randint(0, old - 18))
        stashHobi = str(random.randint(0, old - 10))
        old = str(old)

        tatras = Image.open("pich/cardjpg.jpg")
        idraw = ImageDraw.Draw(tatras)
        font = ImageFont.truetype('arial.ttf', size=28)
        fill = ('#1c1c1c')

        propysk = 30
        propyskVisota = 20
        dopPropysk = 30
        if len(Комнаты_базовая) - len(self.Комнаты) > 3:
            dopPropysk = 30
        text = 'КАРТОЧКА БУНКЕРА'
        idraw.text((10 + propyskVisota, 10+ propysk * 1), text, font=font, fill=fill)
        text = self.БункерКатастрофа
        idraw.text((10 + propyskVisota, 10 + propysk * 2), text, font=font, fill=fill)
        text = self.БункерМестанахождение
        idraw.text((10 + propyskVisota, 10 + propysk * 3), text, font=font, fill=fill)
        text = self.БункерКомнаты
        idraw.text((10 + propyskVisota, 10 + propysk * 4), text, font=font, fill=fill)
        text = self.БункерПредметы
        idraw.text((10 + propyskVisota, 10 + propysk * 5 + dopPropysk), text, font=font, fill=fill)
        text = self.БункерДебафы
        idraw.text((10 + propyskVisota, 10 + propysk * 6 + dopPropysk), text, font=font, fill=fill)
        text = self.БункерРазрушаемость
        idraw.text((10 + propyskVisota, 10 + propysk * 7 + dopPropysk), text, font=font, fill=fill)
        text = self.БункерВремя
        idraw.text((10 + propyskVisota, 10 + propysk * 8 + dopPropysk), text, font=font, fill=fill)

        text = 'КАРТОЧКА ИГРОКА'
        idraw.text((10 + propyskVisota, 10 + propysk * 11 + dopPropysk), text, font=font, fill=fill)
        text = 'Профессия: ' + self.Профессии.pop(random.randint(0, len(self.Профессии) - 1)) + " (стаж " + stash + " лет)"
        idraw.text((10 + propyskVisota, 10 + propysk * 12 + dopPropysk), text, font=font, fill=fill)
        text = 'Пол: ' + str(self.Пол[random.randint(0, len(self.Пол) - 1)]) + " Возраст: " + old
        idraw.text((10 + propyskVisota, 10 + propysk * 13 + dopPropysk), text, font=font, fill=fill)
        text = 'Фобия: ' + self.Фобии.pop(random.randint(0, len(self.Фобии) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 14 + dopPropysk), text, font=font, fill=fill)
        text = 'Здоровье: ' + self.Болезнь.pop(random.randint(0, len(self.Болезнь) - 1)) + ' Стадия: ' + self.Болезнь_стадия.pop(
            random.randint(0, len(self.Болезнь_стадия) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 15 + dopPropysk), text, font=font, fill=fill)
        text = 'Телосложение: ' + self.Телосложение[random.randint(0, len(self.Телосложение) - 1)]
        idraw.text((10 + propyskVisota, 10 + propysk * 16 + dopPropysk), text, font=font, fill=fill)
        text = 'Человеческая черта: ' + self.Человеческая_черта.pop(random.randint(0, len(self.Человеческая_черта) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 17 + dopPropysk), text, font=font, fill=fill)
        text = 'Хобби: ' + self.Хобби.pop(random.randint(0, len(self.Хобби) - 1)) + " (стаж " + stash + " лет)"
        idraw.text((10 + propyskVisota, 10 + propysk * 18 + dopPropysk), text, font=font, fill=fill)
        text = 'Багаж: ' + self.Багаж.pop(random.randint(0, len(self.Багаж) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 19 + dopPropysk), text, font=font, fill=fill)
        text = 'ДопИнф: ' + self.ДопИнф.pop(random.randint(0, len(self.ДопИнф) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 20 + dopPropysk), text, font=font, fill=fill)
        text = 'Карта1: ' + self.Карта1.pop(random.randint(0, len(self.Карта1) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 21 + dopPropysk), text, font=font, fill=fill)
        text = 'Карта2: ' + self.Карта2.pop(random.randint(0, len(self.Карта2) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 22 + dopPropysk), text, font=font, fill=fill)

        dopPropysk2 = 0
        for i in self.RodSvaz:
            if i[0] == id:
                user_get = vk.users.get(user_ids=(i[1]))
                user_get = user_get[0]
                first_name = user_get['first_name']  # Имя пользователя
                last_name = user_get['last_name']  # Фамилия
                fullname = first_name + ' ' + last_name
                text = 'Также ' + fullname + " является вам: " + i[2]
                idraw.text((10 + propyskVisota, 10 + propysk * 22 + dopPropysk + dopPropysk2), text, font=font)
                dopPropysk2 += propysk

            if i[1] == id:
                user_get = vk.users.get(user_ids=(i[0]))
                user_get = user_get[0]
                first_name = user_get['first_name']  # Имя пользователя
                last_name = user_get['last_name']  # Фамилия
                fullname = first_name + ' ' + last_name
                text = 'Также ' + fullname + " является вам: " + i[2]
                idraw.text((10 + propyskVisota, 10 + propysk * 22 + dopPropysk + dopPropysk2), text, font=font)
                dopPropysk2 += propysk

        tatras.save('card.jpg')

        doc(id, "Карта №" + str(self.card_count))
        self.card_count += 1

    def startGame(self):
        self.initCard()
        for i in self.user:
            self.create_card(i)

    def RandomPlayer(self):
        rand1 = random.choice(self.user)
        sender(rand1, 'Поздравляю вам повезло... Ну или не очень...')

    def createUserRodSvaz(self):
        colRodSvaz = random.randint(0,2)
        for i in range(colRodSvaz):
            rand1 = random.choice(self.user)
            rand2 = random.choice(self.user)
            self.RodSvaz.append([rand1, rand2, self.РодственныеСвязи.pop(random.randint(0, len(self.РодственныеСвязи) - 1))])

    def StartVote(self):
        self.VoteLen = len(self.user)
        self.voteList = []
        for i in self.user:
            self.voteList.append([i, 0])
            keyboard = VkKeyboard(one_time=True)
            lenButton = 0
            for j in self.user:
                if i != j:
                    user_get = vk.users.get(user_ids=(j))
                    user_get = user_get[0]
                    first_name = user_get['first_name']  # Имя пользователя
                    last_name = user_get['last_name']  # Фамилия
                    fullname = first_name + ' ' + last_name
                    if lenButton == 3:
                        keyboard.add_line()
                        lenButton = 0
                    keyboard.add_button(fullname, color=VkKeyboardColor.SECONDARY)
                    lenButton += 1
            sender(i, 'Хост начал голосование', keyboard.get_keyboard())

    def Vote(self, text, room):
        self.VoteLen -= 1
        for i in self.voteList:
            user_get = vk.users.get(user_ids=(i[0]))
            user_get = user_get[0]
            first_name = user_get['first_name']  # Имя пользователя
            last_name = user_get['last_name']  # Фамилия
            fullname = first_name + ' ' + last_name
            if fullname.lower() == text:
                i[1] += 1

        if self.VoteLen == 0:
            maxVote = -1
            for i in self.voteList:
                if i[1] > maxVote:
                    maxVote = i[1]
            for i in self.voteList:
                if i[1] == maxVote:
                    user_get = vk.users.get(user_ids=(i[0]))
                    user_get = user_get[0]
                    first_name = user_get['first_name']  # Имя пользователя
                    last_name = user_get['last_name']  # Фамилия
                    fullname = first_name + ' ' + last_name
                    for j in self.user:
                        sender(j, 'В голосовании победил: ' + fullname, get_keyboard("войти в комнату"))
            room["Room_status"] = "Создана"

    def getNewHar(self, text):
        sendText = ""
        if text == "бункер комната":
            sendText = "Новая комната бункера: " + self.БункерКомнаты + self.Комнаты.pop(random.randint(0, len(self.Комнаты) - 1))
        if text == "бункер дебаф":
            sendText = "Новый дебаф бункера: " + self.Дебафы.pop(random.randint(0, len(self.Дебафы) - 1))
        if text == "бункер предметы":
            sendText = "Новый предмет в бункере: " + self.ПредметыБункера.pop(random.randint(0, len(self.ПредметыБункера) - 1))
        if text == "профессия":
            sendText = 'Профессия: ' + self.Профессии.pop(random.randint(0, len(self.Профессии) - 1))
        if text == "пол":
            old = random.randint(1, 80)
            if old < 18:
                old = 18
            stash = str(random.randint(0, old - 18))
            stashHobi = str(random.randint(0, old - 10))
            old = str(old)

            sendText = '\nПол: ' + str(self.Пол[random.randint(0, len(self.Пол) - 1)]) + " Возраст: " + old + ' Плодовитость: ' + str(self.Плодовитость[random.randint(0, len(self.Плодовитость) - 1)]) + "\nСтаж работы: " + stash + " Стаж хобби: " + stashHobi
        if text == "фобия":
            sendText = '\nФобия: ' + self.Фобии.pop(random.randint(0, len(self.Фобии) - 1))
        if text == "здоровье":
            sendText = '\nЗдоровье: ' + self.Болезнь.pop(random.randint(0, len(self.Болезнь) - 1)) + ' Стадия: ' + self.Болезнь_стадия.pop(random.randint(0, len(self.Болезнь_стадия) - 1))
        if text == "телосложение":
            sendText = '\nТелосложение: ' + self.Телосложение[random.randint(0, len(self.Телосложение) - 1)]
        if text == "черта":
            sendText = '\nЧеловеческая черта: ' + self.Человеческая_черта.pop(random.randint(0, len(self.Человеческая_черта) - 1))
        if text == "хобби":
            sendText = '\nХобби: ' + self.Хобби.pop(random.randint(0, len(self.Хобби) - 1))
        if text == "багаж":
            sendText = '\nБагаж: ' + self.Багаж.pop(random.randint(0, len(self.Багаж) - 1))
        if text == "доп":
            sendText = '\nДопИнф: ' + self.ДопИнф.pop(random.randint(0, len(self.ДопИнф) - 1))
        if text == "карта1":
            sendText = '\nКарта1: ' + self.Карта1.pop(random.randint(0, len(self.Карта1) - 1))
        if text == "карта2":
            sendText = '\nКарта2: ' + self.Карта2.pop(random.randint(0, len(self.Карта2) - 1))

        sender(id, 'Новая характеристика - ' + sendText,
               get_keyboard("создать комнату"))

def create_cards_count(count, user_id):
    Профессии = Профессия_базовая.copy()
    Фобии = Фобия_базовая.copy()
    Болезнь = Болезнь_базовая.copy()
    Болезнь_стадия = Болезнь_стадия_базовая.copy()
    Телосложение = Телосложение_базовая.copy()
    Человеческая_черта = Человеческая_черта_базовая.copy()
    Хобби = Хобби_базовая.copy()
    Багаж = Багаж_базовая.copy()
    ДопИнф = ДопИнф_базовая.copy()
    Карта1 = Карта1_базовая.copy()
    Карта2 = Карта2_базовая.copy()
    Пол = Пол_базовая.copy()
    Плодовитость = Плодовитость_базовая.copy()
    РодственныеСвязи = РодственныеСвязи_базовая.copy()

    Котострофы = Котострофы_базовая.copy()
    Местанахождение = Местанахождение_базовая.copy()
    Комнаты = Комнаты_базовая.copy()
    ПредметыБункера = ПредметыБункера_базовая.copy()
    Дебафы = Дебафы_базовая.copy()

    БункерКатастрофа = "Катастрофа: " + Котострофы.pop(random.randint(0, len(Котострофы) - 1))
    БункерМестанахождение = "Ваш бункер находится в/под: " + Местанахождение.pop(random.randint(0, len(Местанахождение) - 1))
    БункерРазмер = random.randint(0, 1000)
    Комнат = 0
    БункерКомнаты = "В бункере есть спец. комнаты: "
    if БункерРазмер > 99:
        for i in range(100, БункерРазмер, 100):
            if Комнат < 5:
                БункерКомнаты = БункерКомнаты + Комнаты.pop(random.randint(0, len(Комнаты) - 1)) + ", "
                if Комнат == 2:
                    БункерКомнаты = БункерКомнаты + "\n"
                Комнат = Комнат + 1
    БункерПредметы = "Также в вашем бункере повезло найти: " + ПредметыБункера.pop(random.randint(0, len(ПредметыБункера) - 1))
    БункерДебафы = "Но к сожалению в вашем бункере есть: " + Дебафы.pop(random.randint(0, len(Дебафы) - 1))
    БункерРазрушаемость = "И его разрушенность: " + str(random.randint(0, 40)) + "%"
    БункерВремя = "В этом бункере вам нужно пробыть " + str(random.randint(0, 30)) + " лет. В бункере есть пища строго на этот период для 4 людей.\nКогда вы выйдете из бункера на земле можно будет относительно безопасно жить."

    RodSvaz = []
    ColRodSvaz = random.randint(0,2)
    for i in range(ColRodSvaz):

        rand1 = random.randint(0,count - 1)
        rand2 = random.randint(0,count - 1)

        RodSvaz.append([rand1, rand2,
                             РодственныеСвязи.pop(random.randint(0, len(РодственныеСвязи) - 1))])

    for i in range(count):

        old = random.randint(1, 80)
        if old < 18:
            old = 18
        stash = str(random.randint(0, old - 18))
        stashHobi = str(random.randint(0, old - 10))
        old = str(old)

        tatras = Image.open("pich/cardjpg.jpg")
        idraw = ImageDraw.Draw(tatras)
        font = ImageFont.truetype('arial.ttf', size=28)
        fill = ('#1c1c1c')
        propysk = 30
        dopPropysk = 0
        propyskVisota = 20
        if Комнат > 3:
            dopPropysk = 30
        text = 'КАРТОЧКА БУНКЕРА'
        idraw.text((10 + propyskVisota, 10 + propysk * 1), text, font=font, fill=fill)
        text = БункерКатастрофа
        idraw.text((10 + propyskVisota, 10 + propysk * 2), text, font=font, fill=fill)
        text = БункерМестанахождение
        idraw.text((10 + propyskVisota, 10 + propysk * 3), text, font=font, fill=fill)
        text = БункерКомнаты
        idraw.text((10 + propyskVisota, 10 + propysk * 4), text, font=font, fill=fill)
        text = БункерПредметы
        idraw.text((10 + propyskVisota, 10 + propysk * 5 + dopPropysk), text, font=font, fill=fill)
        text = БункерДебафы
        idraw.text((10 + propyskVisota, 10 + propysk * 6 + dopPropysk), text, font=font, fill=fill)
        text = БункерРазрушаемость
        idraw.text((10 + propyskVisota, 10 + propysk * 7 + dopPropysk), text, font=font, fill=fill)
        text = БункерВремя
        idraw.text((10 + propyskVisota, 10 + propysk * 8 + dopPropysk), text, font=font, fill=fill)

        text = 'КАРТОЧКА ИГРОКА'
        idraw.text((10 + propyskVisota, 10 + propysk * 10 + dopPropysk), text, font=font, fill=fill)
        text = 'Профессия: ' + Профессии.pop(random.randint(0, len(Профессии) - 1)) + " (стаж " + stash + " лет)"
        idraw.text((10 + propyskVisota, 10 + propysk * 11 + dopPropysk), text, font=font, fill=fill)
        text = 'Пол: ' + str(Пол[random.randint(0, len(Пол) - 1)]) + " Возраст: " + old + ' Плодовитость: ' + str(Плодовитость[random.randint(0, len(Плодовитость) - 1)])
        idraw.text((10 + propyskVisota, 10 + propysk * 12 + dopPropysk), text, font=font, fill=fill)
        text = 'Фобия: ' + Фобии.pop(random.randint(0, len(Фобии) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 13 + dopPropysk), text, font=font, fill=fill)
        text = 'Здоровье: ' + Болезнь.pop(random.randint(0, len(Болезнь) - 1)) + ' Стадия: ' + Болезнь_стадия.pop(random.randint(0, len(Болезнь_стадия) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 14 + dopPropysk), text, font=font, fill=fill)
        text = 'Телосложение: ' + Телосложение[random.randint(0, len(Телосложение) - 1)]
        idraw.text((10 + propyskVisota, 10 + propysk * 15 + dopPropysk), text, font=font, fill=fill)
        text = 'Человеческая черта: ' + Человеческая_черта.pop(random.randint(0, len(Человеческая_черта) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 16 + dopPropysk), text, font=font, fill=fill)
        text = 'Хобби: ' + Хобби.pop(random.randint(0, len(Хобби) - 1)) + " (стаж " + stash + " лет)"
        idraw.text((10 + propyskVisota, 10 + propysk * 17 + dopPropysk), text, font=font, fill=fill)
        text = 'Багаж: ' + Багаж.pop(random.randint(0, len(Багаж) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 18 + dopPropysk), text, font=font, fill=fill)
        text = 'ДопИнф: ' + ДопИнф.pop(random.randint(0, len(ДопИнф) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 19 + dopPropysk), text, font=font, fill=fill)
        text = 'Карта1: ' + Карта1.pop(random.randint(0, len(Карта1) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 20 + dopPropysk), text, font=font, fill=fill)
        text = 'Карта2: ' + Карта2.pop(random.randint(0, len(Карта2) - 1))
        idraw.text((10 + propyskVisota, 10 + propysk * 21 + dopPropysk), text, font=font, fill=fill)

        dopPropysk2 = 0
        for j in RodSvaz:
            if j[0] == i:
                text = "Также игрок " + str(j[1] + 1) + " является вам: " + j[2]
                idraw.text((10 + propyskVisota, 10 + propysk * 22 + dopPropysk + dopPropysk2), text, font=font, fill=fill)
                dopPropysk2 += propysk

            if j[1] == i:
                text = "Также игрок " + str(j[0] + 1) + " является вам: " + j[2]
                idraw.text((10 + propyskVisota, 10 + propysk * 22 + dopPropysk + dopPropysk2), text, font=font, fill=fill)
                dopPropysk2 += propysk

        tatras.save('card.jpg')

        doc(user_id, "Карта №" + str(i + 1))
    sender(id, "Создание завершено", get_keyboard("начать"))

def sender(id, text, keyboard = ""):
    if keyboard == "":
        vk.messages.send(user_id=id,
                         message=text,
                         random_id=0)
    else:
        vk.messages.send(user_id = id,
                     message = text,
                     keyboard = keyboard,
                     random_id = 0)

def get_keyboard(command= "начать"):
    keyboard = VkKeyboard(one_time=True)


    if command == "начать" or command == "удалить комнату" or command == "выйти из комнаты":
        keyboard.add_button('Создать комнату', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('Войти в комнату', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Создать карты', color= VkKeyboardColor.PRIMARY)


    if command == "создать комнату":
        keyboard.add_button('Раздать карты всем', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Заменить характеристику', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('Перераздать проф.', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Карта хода', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('Случайный игрок', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Начать голосование', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('Удалить комнату', color=VkKeyboardColor.NEGATIVE)

    if command == "войти в комнату":
        keyboard.add_button('Выйти из комнаты', color=VkKeyboardColor.NEGATIVE)

    if command == "новая характеристика":
        keyboard.add_button("профессия")
        keyboard.add_button("пол")
        keyboard.add_button("фобия")
        keyboard.add_button("здоровье")
        keyboard.add_line()
        keyboard.add_button("телосложение")
        keyboard.add_button("черта")
        keyboard.add_button("хобби")
        keyboard.add_button("багаж")
        keyboard.add_line()
        keyboard.add_button("доп")
        keyboard.add_button("карта1")
        keyboard.add_button("карта2")
        keyboard.add_line()
        keyboard.add_button("бункер комната")
        keyboard.add_button("бункер дебаф")
        keyboard.add_button("бункер предметы")


    return  keyboard.get_keyboard()

def createRoom(id):
    room_id = random.randint(0,9)*1 + random.randint(0,9)*10 + random.randint(0,9)*100 + random.randint(0,9)*1000
    ROOM.append({"Room_id": room_id,
                 "Room_status": "Создана",
                 "User": [id],
                 "Game": GameRom(id, room_id, [id])})
    return room_id

def loginRoom(msg, id):
    tRom = False
    for i in ROOM:
        if str(i["Room_id"]) == msg:
            tRom = True
            game = i["Game"]
            Host = i["User"][0]

    if tRom:
        game.appendUser(id)
        sender(Host, "Подключен новый пользователь\nВсего: " + str(game.lenUser()))
        sender(id, "Подключение успешно\nВаш номер: " + str(game.lenUser()), get_keyboard("войти в комнату"))
    else:
        sender(id, "Неверный код", get_keyboard("начать"))

    return  tRom



for event in longPool.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            try:
                msg = event.text.lower()
                id = event.user_id
                status = "0"
                room_id = 0

                check_profile = os.path.exists(users_dir + str(event.user_id) + ".json")
                if check_profile != True:
                    auth.reg(event.user_id)
                    sender(id, "Привет! Зайди в свободную комнату или создай свою для игры\n Или просто сгенерируй карты", get_keyboard("начать"))
                    continue

                USER_Date = auth.check_user_mention(event.user_id)
                status = USER_Date["Status"]
                room_id = USER_Date["Room_id"]

                if (msg == "начать" and status == "0"):
                    sender(id, "Привет! Зайди в свободную комнату или создай свою для игры\n Или просто сгенерируй карты", get_keyboard("начать"))
                    continue

                if (msg == "сброс"):
                    set_status_userData(USER_Date, "СтартовоеМеню")
                    sender(id, "Привет! Зайди в свободную комнату или создай свою для игры\n Или просто сгенерируй карты", get_keyboard("начать"))
                    continue

                Initvote = False
                for i in ROOM:
                    for j in i["Game"].user:
                        if j == id and i["Room_status"] == "Идет голосование":
                            i["Game"].Vote(msg, i)
                            sender(id, "Голос засчитан", get_keyboard("войти в комнату"))
                            Initvote = True

                if Initvote:
                    continue

                if status == "МеняетХарактеристику":
                    for i in ROOM:
                        if i["User"][0] == id:
                            i["Game"].getNewHar(msg)
                            USER_Date = set_status_userData(USER_Date, "ВКомнатеХост")


                elif status == "СоздаетКарты":
                    USER_Date = set_status_userData(USER_Date, "СтартовоеМеню")
                    try:
                        create_cards_count(int(msg), id)
                    except:
                        sender(id, "Ошибка: в след. раз вводите число", get_keyboard("начать"))

                elif msg == "заменить характеристику" and status == "ВКомнатеХост":
                    USER_Date = set_status_userData(USER_Date, "МеняетХарактеристику")
                    sender(id, "Ввыберите характеристику", get_keyboard("новая характеристика"))

                elif msg == "раздать карты всем" and status == "ВКомнатеХост":
                    for i in ROOM:
                        if i["User"][0] == id:
                            i["Game"].startGame()
                            sender(id, "Карты розданы", get_keyboard("создать комнату"))

                elif msg == "начать голосование" and status == "ВКомнатеХост":
                    for i in ROOM:
                        if i["User"][0] == id:
                            i["Game"].StartVote()
                            i["Room_status"] = "Идет голосование"

                elif msg == "перераздать проф." and status == "ВКомнатеХост":
                    for i in ROOM:
                        if i["User"][0] == id:
                            i["Game"].resetProf()
                            sender(id, "Выполнено", get_keyboard("создать комнату"))
                elif msg == "случайный игрок" and status == "ВКомнатеХост":
                    for i in ROOM:
                        if i["User"][0] == id:
                            i["Game"].RandomPlayer()
                            sender(id, "Выполнено", get_keyboard("создать комнату"))

                elif msg == "карта хода" and status == "ВКомнатеХост":
                    for i in ROOM:
                        if i["User"][0] == id:
                            i["Game"].GetCardStep()
                            sender(id, "Выполнено", get_keyboard("создать комнату"))

                elif msg == "удалить комнату" and status == "ВКомнатеХост":
                    rem = {}
                    for i in ROOM:
                        if i["User"][0] == id:
                            user =  i["Game"].user
                            rem = i
                    ROOM.remove(rem)
                    for id in user:
                        USER_Date = set_status_userData(USER_Date, "СтартовоеМеню")
                        sender(id, "Комната удалена", get_keyboard("начать"))

                elif status == "ВходВКомнату":
                    if loginRoom(msg, id):
                        USER_Date = set_status_userData(USER_Date, "ВКомнате")
                    else:
                        USER_Date = set_status_userData(USER_Date, "СтартовоеМеню")

                elif msg == "выйти из комнаты" and status == "ВКомнате":
                    for i in ROOM:
                        if i["Game"].testUser(id):
                            i["Game"].remUser(id)
                            USER_Date = set_status_userData(USER_Date, "СтартовоеМеню")
                            sender(id, "Вы вышли из комнаты", get_keyboard("начать"))

                elif (msg == "вернуть" and status == "ВКомнатеХост") or (msg == "вернуть" and status == "ВКомнате"):
                    if status == "ВКомнатеХост":
                        kb = get_keyboard("создать комнату")
                    if status == "ВКомнате":
                        kb = get_keyboard("войти в комнату")
                    sender(id, "...", kb)


                elif msg == "создать комнату" and status == "СтартовоеМеню":
                    sender(id, "Комната создана\nКод подключения: " + str(createRoom(id)), get_keyboard("создать комнату"))
                    USER_Date = set_status_userData(USER_Date, "ВКомнатеХост")

                elif msg == "войти в комнату" and status == "СтартовоеМеню":
                    sender(id, "Введите код")
                    USER_Date = set_status_userData(USER_Date, "ВходВКомнату")

                elif msg == "создать карты" and status == "СтартовоеМеню":

                    set_status_userData(USER_Date, "СоздаетКарты")

                    sender(id, "Введите количество", get_keyboard())
                else:

                        if status == "ВКомнатеХост":
                            kb = get_keyboard("создать комнату")
                        elif status == "ВКомнате":
                            kb = get_keyboard("войти в комнату")
                        elif status == "МеняетХарактеристику":
                            kb = get_keyboard("новая характеристика")
                        else:
                            kb = get_keyboard("начать")
                        sender(id, "Я хз что тебе ответить на это...\nПопробуй написать еще", kb)
            except:
                sender(id, "Не знаю как, но только что вы сломали бота. Не делайте так больше и сообщите пожалуйста разработчику об ошибке.")

