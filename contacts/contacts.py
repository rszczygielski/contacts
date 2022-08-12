from myLogger.myLogger import Logger
from enum import Enum, auto
import os
# testy jednostkowe i intregracyjne, jednoskowe to takie które kod testuje sam siebie, a integracujne to są takie które są napisane w innym programie

class NumberType(Enum):
    WORK = "WORK"
    FAX = "FAX"
    PERSONAL = "PERSONAL"
    MOBILE = "MOBILE"
    HOME = "HOME"

class EmailType(Enum):
    WORK = "WORK"
    PERSONAL = "PERSONAL"
    UNIVERISTY = "UNIVERSITY"

class Contacts():
    def __init__(self, contactFile:str):
        self.contacts = []
        self.contactFile = contactFile
        self.readContacts()
    
    def saveingDecorator(method):

        def save(self, *args):
            result = method(self, *args)
            self.saveFile()
            Logger.INFO("File was saved")
            return result
        return save

    @saveingDecorator
    def addContact(self, firstName:str, lastName:str, *newNumbersOrEmails):
        """Adds contact to the list of contacts

        Args:
            firstName (str): contact first name
            lastName (str): contact last name
        """
        numbersStructList = []
        eMailsStructList = []
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                Logger.WARNING("Contact already exsists")
                return
        for newNumberOrEmail in newNumbersOrEmails:
            #newNumbersOrEmail = list of numbers structs or email structs
            if isinstance(newNumberOrEmail, Number):
                newNumberStruct = newNumberOrEmail
                for contact in self.contacts:
                    for numberStruct in contact.numbers:
                        if newNumberStruct.number == numberStruct.number:
                            Logger.WARNING("This number already exists")
                            return
                numbersStructList.append(newNumberStruct)
            if isinstance(newNumberOrEmail, Email):
                newEmailStruct = newNumberOrEmail
                for contact in self.contacts:
                    for emailStruct in contact.emails:
                        if newEmailStruct.email == emailStruct.email:
                            Logger.WARNING("This email already exists")
                            return
                eMailsStructList.append(newEmailStruct)
        self.contacts.append(Contact(firstName, lastName, numbersStructList, eMailsStructList))

    def saveFile(self):
        """Saves contacts to file
        """
        contactFile = open(self.contactFile, "w")
        for contact in self.contacts:
            contactLine = f"{contact}\n"
            contactFile.write(contactLine)
        contactFile.close()

    def readContacts(self):
        """Reads contacts form file
        """
        if not os.path.isfile(self.contactFile):
            Logger.WARNING("There is no such file as contacts.txt")
            return  
        with open(self.contactFile) as readFile:
            lines = readFile.readlines()
        if len(lines) == 0:
            Logger.WARNING("There is no contacts in file")
        else:
            for line in lines:
                line = line.strip()
                splitedLine = line.split()
                firstName = splitedLine[0]
                lastName = splitedLine[1]
                numbersAndEmails = splitedLine[2:]
                # spliting all emails and numbers to one list
                numberStructList = []
                emailStructList = []
                for numberOrEmail in numbersAndEmails:
                    if "@" in numberOrEmail:
                        # creating a new structure of email
                        emailStructList.append(Email.initFromString(numberOrEmail))
                        # adding an email struct to list of email structs
                    else:
                        # creating a new structure of number
                        numberStructList.append(Number.initFromString(numberOrEmail))
                        # adding an number struct to list of number structs
                self.contacts.append(Contact(firstName, lastName, numberStructList, emailStructList))
            
    def showContacts(self):
        """Prints contacts in terminal
        """
        for contact in self.contacts:
            print(contact)
                
    @saveingDecorator
    def addNumberToContact(self, firstName, lastName, numberStructList:list):
        """Adds number to contact

        Args:
            firstName (str): first name of already exsisting contact
            lastName (_type_): last name of already exsisting contact
            numberStructList (list): list of number structs (Number class)
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                for numberStruct in numberStructList:
                    contact.numbers.append(numberStruct)

    @saveingDecorator
    def addEmailToContact(self, firstName, lastName, emailStructList:list):
        """_summary_

        Args:
            firstName (_type_): first name of already exsisting contact
            lastName (_type_): last name of already exsisting contact
            emailStructList (list): list of emails structs (Email class)
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                for emailStruct in emailStructList:
                    contact.emails.append(emailStruct)
    
    def getContactNumbers(self, firstName, lastName):
        """Returns contacts numbers

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact

        Returns:
            list: list of number sctucts (Number class)
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                return contact.numbers
    
    def getContactEmails(self, firstName, lastName):
        """Returns contacts emails

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact

        Returns:
            list: list of email sctucts (Email class)
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                return contact.emails
               
    def searchForContactNumber(self, number):
        """Prints contact with given number

        Args:
            number (int): number to search
        """
        for contact in self.contacts:
            for numberStruct in contact.numbers:
                if number in numberStruct.number:
                    print(contact.firstName, contact.lastName, numberStruct.number, numberStruct.numberType.name)

    @saveingDecorator
    def sortContactsByFirstName(self):
        """Sorts contacts by first name
        """
        def GetFirstName(contact):
            return contact.firstName
        self.contacts.sort(key=GetFirstName)
    
    @saveingDecorator
    def sortContactsByLastName(self):
        """Sorts contacts by last name
        """
        def GetLastName(contact):
            return contact.lastName
        self.contacts.sort(key=GetLastName)

    @saveingDecorator
    def deleteContact(self, firstName, lastName):
        """Deletes contact from list of contact structs (Contact class)

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                self.contacts.remove(contact)
                Logger.INFO(f"Contact has been deleted")
                return
        Logger.WARNING(f"Contacnt not exsist")
    
    def getContact(self, name):
        """Returns contact struct

        Args:
            name (str): first name and last name or only last name or only first name

        Returns:
            class: contact (class Contact)
        """
        listOfContacts = []
        splitedName = name.split()
        if len(splitedName) == 2:
            for contact in self.contacts:
                if contact.firstName == splitedName[0] and contact.lastName == splitedName[1]:
                    listOfContacts.append(contact)
        elif len(splitedName) == 1:
            for contact in self.contacts:
                if contact.firstName == name or contact.lastName == name:
                        listOfContacts.append(contact)
        if len(listOfContacts) == 1:
            return listOfContacts[0]
        elif len(listOfContacts) > 1:
            Logger.WARNING(f"There is more contacts")
        Logger.WARNING(f"Contacnt not exsist")
   
    def lookingForContact(self, name):
        """Returns contact struct

        Args:
            name (str): first name and last name or only last name or only first name

        Returns:
            class: contact (class Contact)
        """
        listOfContacts = self.lookingForContacts(name)
        if len(listOfContacts) == 1:
            return listOfContacts[0]
        elif len(listOfContacts) > 1:
            Logger.WARNING(f"There is more contacts")
        else:
            Logger.WARNING(f"Contacnt not exsist")
    
    def lookingForContactByFirstOrName(self, name):
        """Returns contacts with the same name

        Args:
            name (str): full name or part of the name

        Returns:
            list: list of contact structs (Contact class)
        """
        listOfContacts = []
        for contact in self.contacts:
            if name in contact.firstName or name in contact.lastName:
                listOfContacts.append(contact)
        return listOfContacts

    def lookingForContactByFullName(self, firstName, lastName):
        """Returns contact by full name 

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact

        Returns:
            list: list of contact structs (class Contact)
        """
        listOfContacts = []
        for contact in self.contacts:
            if firstName in contact.firstName and lastName in contact.lastName:
                listOfContacts.append(contact)
        return listOfContacts

    def lookingForContacts(self, name):
        """Return list of contact structs (Contact class)

        Args:
            name (str): full name or only first name or only last name

        Returns:
            list: list of conract structs (class Contact)
        """
        splitedName = name.split()
        listOfContacts = []
        if len(splitedName) == 1:
            listOfContacts.extend(self.lookingForContactByFirstOrName(name))
        elif len(splitedName) == 2:
            listOfContacts.extend(self.lookingForContactByFullName(splitedName[0], splitedName[1]))
        if len(listOfContacts) == 0:
            Logger.WARNING(f"Contact not exsist")
        else:
            return listOfContacts

    @saveingDecorator
    def deleteNumber(self, firstName, lastName, numberToDel):
        """Deletes contact number

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact
            numberToDel (int): number to be deleted
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                for number in contact.numbers:
                    if number.number == numberToDel:
                        contact.numbers.remove(number)
                        return
                Logger.WARNING("This contact don't have such number")
                return
        Logger.WARNING("There is no such contact")
    
    @saveingDecorator
    def deleteEmail(self, firstName, lastName, emailToDel):
        """Deletes contact email

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact
            emailToDel (email): email to be deleted
        """
        for contact in self.contacts:
            if contact.firstName == firstName and contact.lastName == lastName:
                for email in contact.emails:
                    if email.email == emailToDel:
                        contact.emails.remove(email)
                        return
                Logger.WARNING("This contact don't have such email")
                return
        Logger.WARNING("There is no such contact")

    def getDefaultNumber(self, firstName, lastName):
        """Returns default number

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact

        Returns:
            int: default number for given contact 
        """
        for contact in self.contacts:
            if firstName == contact.firstName and lastName == contact.lastName and len(contact.numbers) > 0:
                    return contact.numbers[0]
        Logger.WARNING("There is no such contact or such number")

    def getDefaultEmail(self, firstName, lastName):
        """Returns default email

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact

        Returns:
            str: default number for given contact
        """
        for contact in self.contacts:
            if firstName == contact.firstName and lastName == contact.lastName and len(contact.emails) > 0:
                return contact.emails[0].email
        Logger.WARNING("There is no such contact or such email")

    @saveingDecorator
    def changeDefaultNumber(self, firstName, lastName, newDefaultNumber):
        """Changes default number for given contact

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact
            newDefaultNumber (int): number to be set as a default one
        """
        for contact in self.contacts:
            if firstName == contact.firstName and lastName == contact.lastName and len(contact.numbers) > 0:
                for number in contact.numbers:
                    if number.number == newDefaultNumber:
                        contactNumberIndex = contact.numbers.index(number)
                        contact.numbers.insert(0, contact.numbers.pop(contactNumberIndex))
                        return
                Logger.WARNING("This contact don't have such number")
        Logger.WARNING("There is no such contact")

    @saveingDecorator
    def changeDefaultEmail(self, firstName, lastName, newDefaultEmail):
        """Changes default email for given contact

        Args:
            firstName (str): first name of already exsisting contact
            lastName (str): last name of already exsisting contact
            newDefaultEmail (str): email to be set as a default one
        """
        for contact in self.contacts:
            if firstName == contact.firstName and lastName == contact.lastName and len(contact.emails) > 0:
                for email in contact.emails:
                    if email.email == newDefaultEmail:
                        contactEmailIndex = contact.emails.index(email)
                        contact.emails.insert(0,contact.emails.pop(contactEmailIndex))
                        return
                Logger.WARNING("This contact don't have such number")
        Logger.WARNING("There is no such contact")
    

class Contact():
    def __init__(self, firstName, lastName, numbers:list, emails:list):
        self.firstName = firstName
        self.lastName = lastName
        self.numbers = numbers
        self.emails = emails
    
    def __getitem__(self, index):
        if index == 0:
            return self.firstName
        if index == 1:
            return self.lastName
        if index == 2:
            return self.numbers
        if index == 3:
            return self.emails
        if index > 3:
            raise IndexError
    
    def __str__(self):
        stringToPrint = f"{self.firstName} {self.lastName}"
        for number in self.numbers:
            stringToPrint += f" {number}"
        for email in self.emails:
            stringToPrint += f" {email}"
        return stringToPrint

class Email():
    def __init__(self, email, emailType:EmailType = EmailType.PERSONAL):
        if "@" not in email:
            raise ValueError("Not correct email, no @ in email") 
        self.email = email
        self.emailType = emailType

    def __str__(self) -> str:
        return f"{self.emailType.name}:{self.email}"

    @classmethod
    def initFromString(cls, emailString):
        """Initialization from string

        Args:
            emailString (str): string to init Email class

        Raises:
            ValueError: Email don't contain :
            ValueError: There is no such email type

        Returns:
            class: Email class
        """
        if ":" not in emailString:
            raise ValueError("Email don't contain :")
        emailTypes =[emailType.value for emailType in EmailType]
        splitedEmail = emailString.split(":")
        emailType = splitedEmail[0]
        email = splitedEmail[1]
        if emailType not in emailTypes:
            raise ValueError("There is no such email type")
        return cls(email, EmailType(emailType))

class Number():
    def __init__(self, number:str, numberType:NumberType = NumberType.MOBILE):
        if len(number) != 9:
            raise ValueError("Number not correct, number has to have nine digits")
        self.number = number
        self.numberType = numberType
    
    def __str__(self) -> str:
        return f"{self.numberType.name}:{self.number}"
    
    @classmethod
    def initFromString(cls, numberString):
        """Initialization from string

        Args:
            numberString (str): string to init Number class

        Raises:
            ValueError: Number don't contain :
            ValueError: There is no such number type

        Returns:
            class: Number class
        """
        if ":" not in numberString:
            raise ValueError("Number don't contain :")
        numberTypes = [numberType.value for numberType in NumberType]
        splitedNumber = numberString.split(":")
        numberType = splitedNumber[0]
        number = splitedNumber[1]
        if numberType not in numberTypes:
            raise ValueError("There is no such number type")
        return cls(number, NumberType(numberType))

class TerminalUser():
    """Interactive mode class, uses class methods without possitionl arguments but with input instead
    """
    def __init__(self):
        self.phone = Contacts("contacts.txt")
    
    def showContacts(self):
        self.phone.showContacts()

    def addContacts(self):
        firstName = input("First name: ")
        lastName = input("Last name: ")
        newNumber = input("New number: ")
        newEmail = input("New email: ")
        self.phone.addContact(firstName, lastName, Number(newNumber), Email(newEmail))
    
    def addNumberToContact(self):
        firstName = input("First Name: ")
        lastName = input("Last Name: ")
        howManyNumbersToAdd = int(input("How many numbers you want to add: "))
        numberStructList = []
        for _ in range(howManyNumbersToAdd):
             newNumber = input("Number to add: ")
             numberStructList.append(Number(newNumber))
        self.phone.addNumberToContact(firstName, lastName, numberStructList)
    
    def addEmailToContact(self):
        firstName = input("First Name: ")
        lastName = input("Last Name: ")
        howManyEmailsToAdd = int(input("How many emailss you want to add: "))
        emailStructList = []
        for _ in range(howManyEmailsToAdd):
             newEmail = input("Email to add: ")
             emailStructList.append(Email(newEmail))
        self.phone.addEmailToContact(firstName, lastName, emailStructList)
    
    def deleteContact(self):
        firstName = input("First Name: ")
        lastName = input("Last Name: ")
        self.phone.deleteContact(firstName, lastName)

    def deleteNumber(self):
        firstName = input("First name: ")
        lastName = input("Last name: ")
        numberToDelete = input("Number to delete: ")
        self.phone.deleteNumber(firstName, lastName, numberToDelete)
    
    def deleteEmail(self):
        firstName = input("First name: ")
        lastName = input("Last name: ")
        emailToDelete = input("Email to delete: ")
        self.phone.deleteEmail(firstName, lastName, emailToDelete)


    def exitTerminal(self):
        exit()

class ComendTerminal(Enum):
    SHOW_CONTACTS = auto()
    ADD_CONTACTS = auto()
    ADD_NUMBER_TO_CONTACT = auto()
    ADD_EMAIL_TO_CONTACT = auto()
    DELETE_CONTACT = auto()
    DELETE_NUMBER = auto()
    DELETE_EMAIL = auto()
    EXIT = auto()

if __name__ == "__main__":
    terminal = TerminalUser()
    dictWithMethods = {
        ComendTerminal.SHOW_CONTACTS.value: terminal.showContacts,
        ComendTerminal.ADD_CONTACTS.value: terminal.addContacts,
        ComendTerminal.ADD_NUMBER_TO_CONTACT.value: terminal.addNumberToContact,
        ComendTerminal.ADD_EMAIL_TO_CONTACT.value: terminal.addEmailToContact,
        ComendTerminal.DELETE_CONTACT.value: terminal.deleteContact,
        ComendTerminal.DELETE_NUMBER.value: terminal.deleteNumber,
        ComendTerminal.DELETE_EMAIL.value: terminal.deleteEmail,
        ComendTerminal.EXIT.value: terminal.exitTerminal,
        }
    textInput = "\n"
    for command in ComendTerminal:
        textInput += f"\tPress {command.value} to {command.name}\n"

    while True:
        Logger.settings(show_date=False, show_file_name=False)
        try:
            userInput = int(input(textInput))
        except ValueError:
            Logger.ERROR("WRONG INPUT VALUE")
        try:
            dictWithMethods[userInput]()
        except KeyError:
            Logger.ERROR("WRONG INPUT VALUE")