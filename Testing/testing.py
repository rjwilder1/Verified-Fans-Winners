from faker import Faker
from collections import OrderedDict
from itertools import cycle
import random

linect = 0

locales = OrderedDict([
    ('en-US', 1)
])

fake = Faker(locales)
CardsList = []
TACFullList = []
Accounts = []
def FillCardList():
    global CardsList
    with open("accs.txt", "r") as file:
        for line in file:
            data = line.split(',')
            email = data[0]
            passw = data[1]
            MasterCard = data[2]
            CardNumber = data[3].replace(' ', '')
            ExpMonth = data[4]
            ExpYear = data[5]
            First = data[6]
            Last = data[7]
            Address = data[8]
            BLANK = data[9]
            Town = data[10]
            State = data[11]
            ZipCode = data[12]
            USA = data[13]
            PhoneNumber = data[14]
            with open('Cards.txt', "a") as f:
                f.write(f"{CardNumber},{ExpMonth},{ExpYear}\n")
            CardsList.append(f"{CardNumber},{ExpMonth},{ExpYear}")

def WriteTAC():
    FillCardList()
    with open("TAC.txt", "r") as file:
        for line in file:
            Accounts.append(line.rstrip('\n'))
            linect+=1

    with open('TACWITHCARDS.txt', "w") as file:
        cyclecards = cycle(CardsList)
        for i in range(linect):
            cards = next(cyclecards)
            card = cards.split(',')
            file.write(f"{Accounts[i].split(',')[0]},{Accounts[i].split(',')[1]},MasterCard,{card[0]},{card[1]},{card[2]},{fake.name().split()[0]},{fake.name().split()[1]},{fake.street_address()},,{fake.city()},California,60169,United States,{str(int(''.join(random.sample('2345678901', 10))))}\n")                                 
AYCDCT = 0

def GetCVV(CN):#4 & 7
    with open('AYCDImportCVV.txt', "r") as file:
        for line in file:
            values = line.strip().split(",")
            CardNumber = values[4].replace(' ','')
            if CardNumber in CN:
                return values[7]#CVV
            
def WriteD():
    global AYCDCT
    with open("TACWITHCARDS.txt", "r") as file:
        for line in file:
            TACFullList.append(line.rstrip('\n'))
            AYCDCT+=1

    with open('FullAYCDImport.txt', "w") as file:
        for i in range(AYCDCT):
            email = TACFullList[i].split(',')[0]
            password = TACFullList[i].split(',')[1]
            card = TACFullList[i].split(',')[3]
            last4card = card[-4:]
            cvv = GetCVV(card)
            file.write(f"rj{i},{email},{password},{last4card},{cvv}\n")