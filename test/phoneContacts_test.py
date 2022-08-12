import unittest
import os
import sys
from unittest import TestCase
sys.path.insert(1, '/home/radeksz/Documents/python_VSC/personal_classes/contacts/contacts')
from contacts.contacts import Contacts
from contacts.contacts import Number
from contacts.contacts import NumberType
from contacts.contacts import Email
from contacts.contacts import EmailType
from contacts.contacts import Contact

class PhoneContactsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.contactFile = "/home/radeksz/Documents/python_VSC/personal_classes/contacts/contacts/contactsTest.txt"
        cls.contactFile = "/mnt/c/Users/radek/Desktop/PythonVSD/personal_classes/contacts/contacts/contacts.txt"

    def tearDown(self):
        if os.path.isfile(self.__class__.contactFile):
            os.remove(self.__class__.contactFile)
    
    # def setUp(self):
    #     pass

    @classmethod
    def tearDownClass(cls):
        print("TEST OVER")

    def testPhoneContacts(self):
        phone = Contacts(self.__class__.contactFile)
        self.assertEqual(len(phone.contacts), 0)

    def testAddContact(self):
        phone = Contacts(self.__class__.contactFile)
        lenContacts = len(phone.contacts)
        phone.addContact("firstName","lastName", Number("123457779", NumberType.HOME), Number("123456788", NumberType.MOBILE))
        self.assertEqual(len(phone.contacts), lenContacts+1)
    
    def testAddContactWithWrongNumber(self):
        phone = Contacts(self.__class__.contactFile)
        lenContacts = len(phone.contacts)
        try:
            phone.addContact("firstName","lastName", Number("123456789", NumberType.HOME), Number("12345678910", NumberType.MOBILE))
        except ValueError:
            pass
        self.assertEqual(len(phone.contacts), lenContacts)
        # self.assertRaises(ValueError, phone.addContact,"firstName","lastName", Number("123456789", NumberType.HOME), Number("12345678910", NumberType.MOBILE))
    
    def testIfContactFileIsNotExsist(self):
        phone = Contacts(self.__class__.contactFile)
        self.assertFalse(os.path.isfile(phone.contactFile))
        phone.saveFile()
        self.assertTrue(os.path.isfile(phone.contactFile))
    
    def testAddContactWithTheSameNumber(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName","lastName", Number("123457779", NumberType.HOME), Number("123456788", NumberType.MOBILE))
        lenContacts = len(phone.contacts)
        phone.addContact("firstName2","lastName2", Number("123457779", NumberType.HOME), Number("222222222", NumberType.MOBILE))
        self.assertEqual(len(phone.contacts), lenContacts)
    
    def testAddOnlyNumberToContact(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL))
        contactNumbers = len(phone.getContactNumbers("firstName", "lastName"))
        self.assertEqual(contactNumbers, 1)
        phone.addNumberToContact("firstName", "lastName", [Number("777777777", NumberType.PERSONAL)])
        newNumberList = phone.getContactNumbers("firstName", "lastName")
        self.assertEqual(contactNumbers+1, len(newNumberList))
    
    def testAddOnlyEmailToContact(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Email("test_mail@gmail.com", EmailType.PERSONAL))
        contactEmails = len(phone.getContactEmails("firstName", "lastName"))
        self.assertEqual(contactEmails, 1)
        phone.addEmailToContact("firstName", "lastName", [Email("test_mail2@gmail.com", EmailType.PERSONAL)])
        newEmailList = phone.getContactEmails("firstName", "lastName")
        self.assertEqual(contactEmails+1, len(newEmailList))
    
    
    def testAddContactWithMail(self):
        phone = Contacts(self.__class__.contactFile)
        lenContacts = len(phone.contacts)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        self.assertEqual(len(phone.contacts), lenContacts+1)
    
    def testAddContactWithWrongMail(self):
        phone = Contacts(self.__class__.contactFile)
        lenContacts = len(phone.contacts)
        try:
            phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mailgmail.com", EmailType.PERSONAL))
        except ValueError:
            pass
        self.assertEqual(len(phone.contacts), lenContacts)
    
    def testAddContactWithTheSameMail(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        lenContacts = len(phone.contacts)
        phone.addContact("firstName2", "lastname2", Number("777777777", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.WORK))
        self.assertEqual(len(phone.contacts), lenContacts)
    
    def testSaveToFile(self):
        phone = Contacts(self.__class__.contactFile)
        phone.saveFile()
        with open(phone.contactFile) as contactFile:
            zeroLines = len(contactFile.readlines())
        self.assertEqual(zeroLines, 0)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        phone.saveFile()
        with open(phone.contactFile) as contactFile:
            newLineFileLen = len(contactFile.readlines())
        self.assertEqual(newLineFileLen, 1)
        self.assertNotEqual(zeroLines, newLineFileLen)
        self.assertEqual(zeroLines+1, newLineFileLen)
    
    def testReadContacts(self):
        phone = Contacts(self.__class__.contactFile)
        phone.saveFile()
        phone.readContacts()
        zeroContacts = len(phone.contacts)
        self.assertEqual(zeroContacts, 0)
        with open(phone.contactFile, "w") as contactFile:
            contactFile.write("firstName lastName PERSONAL:888888888 PERSONAL:testmail@test.com ")
        phone.readContacts()
        newContactLen = len(phone.contacts)
        self.assertEqual(newContactLen, 1)
        self.assertNotEqual(zeroContacts, newContactLen)
        self.assertEqual(zeroContacts+1, newContactLen)
    
    def testDeleteContact(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        oneContact = len(phone.contacts)
        self.assertEqual(oneContact, 1)
        phone.deleteContact("firstName", "lastName")
        self.assertEqual(len(phone.contacts), 0)
        self.assertNotEqual(len(phone.contacts), oneContact)
    
    def testDeleteContactNotExsist(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        oneContact = len(phone.contacts)
        self.assertEqual(oneContact, 1)
        phone.deleteContact("firstName2", "lastName2")
        self.assertEqual(len(phone.contacts), 1)
    
    def testGetContactFirstAndLastName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contact = phone.getContact("firstName lastName")
        self.assertEqual(contact.firstName, "firstName")
        self.assertEqual(contact.lastName, "lastName")
    
    def testGetContactFirstName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contact = phone.getContact("firstName")
        self.assertEqual(contact.firstName, "firstName")
        self.assertEqual(contact.lastName, "lastName")
    
    def testGetContactLastName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contact = phone.getContact("lastName")
        self.assertEqual(contact.firstName, "firstName")
        self.assertEqual(contact.lastName, "lastName")
    
    def testSortContactByLastName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "ZZZZlastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        phone.addContact("firstName", "AAAAlastName", Number("890459631", NumberType.PERSONAL), Email("test_mail2@gmail.com", EmailType.PERSONAL))
        self.assertEqual(len(phone.contacts), 2)
        self.assertEqual(phone.contacts[0].lastName, "ZZZZlastName")
        self.assertEqual(phone.contacts[1].lastName, "AAAAlastName")
        phone.sortContactsByLastName()
        self.assertEqual(phone.contacts[0].lastName, "AAAAlastName")
        self.assertEqual(phone.contacts[1].lastName, "ZZZZlastName")
    
    def testSortContactByFirstName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("ZZZZfirstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        phone.addContact("AAAAfirstName", "lastName", Number("890459631", NumberType.PERSONAL), Email("test_mail2@gmail.com", EmailType.PERSONAL))
        self.assertEqual(len(phone.contacts), 2)
        self.assertEqual(phone.contacts[0].firstName, "ZZZZfirstName")
        self.assertEqual(phone.contacts[1].firstName, "AAAAfirstName")
        phone.sortContactsByFirstName()
        self.assertEqual(phone.contacts[0].firstName, "AAAAfirstName")
        self.assertEqual(phone.contacts[1].firstName, "ZZZZfirstName")
    
    def testLookingForContactByFirstName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contactFound = phone.lookingForContact("firstName")
        contactInContacts = phone.getContact("firstName")
        self.assertEqual(contactFound, contactInContacts)
    
    def testLookingForContactByPartOfFirstName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contactFound = phone.lookingForContact("first")
        contactInContacts = phone.getContact("firstName")
        self.assertEqual(contactFound, contactInContacts)

    def testLookingForContactByLastName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contactFound = phone.lookingForContact("lastName")
        contactInContacts = phone.getContact("lastName")
        self.assertEqual(contactFound, contactInContacts)
    
    def testLookingForContactByPartOfLastName(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contactFound = phone.lookingForContact("last")
        contactInContacts = phone.getContact("lastName")
        self.assertEqual(contactFound, contactInContacts)
    
    def testLookingForContactTwoSimilarContacts(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName2", "lastName2", Number("890459631", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        contactFound = phone.lookingForContact("last")
        contactInContacts = phone.getContact("lastName")
        self.assertNotEqual(contactFound, contactInContacts)

    def testLookingForContacts(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        phone.addContact("firstName2", "lastName2", Number("890459631", NumberType.PERSONAL), Email("test_mail2@gmail.com", EmailType.PERSONAL))
        self.assertEqual(len(phone.contacts), 2)
        contactFound = phone.lookingForContacts("last")
        contactInContacts = [phone.getContact("lastName"), phone.getContact("lastName2")]
        self.assertEqual(contactFound, contactInContacts)

    def testDeleteNumber(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        self.assertEqual(len(phone.contacts), 1)
        phone.deleteNumber("firstName", "lastName", "890459632")
        self.assertEqual(phone.contacts[0].numbers, [])

    def testDeleteEmail(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        self.assertEqual(len(phone.contacts), 1)
        phone.deleteEmail("firstName", "lastName", "test_mail@gmail.com")
        self.assertEqual(phone.contacts[0].emails, [])

    def testGetDefaultNumberOneNumber(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        defaultNumber = phone.getDefaultNumber("firstName", "lastName")
        numberToChceck = phone.contacts[0].numbers[0]
        self.assertEqual(defaultNumber, numberToChceck)

    def testGetDefaultNumberTwoNumber(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Number("123456789", NumberType.HOME), Email("test_mail@gmail.com", EmailType.PERSONAL))
        defaultNumber = phone.getDefaultNumber("firstName", "lastName")
        numberToChceck = phone.contacts[0].numbers[0]
        secondNumber = phone.contacts[0].numbers[1]
        self.assertEqual(defaultNumber, numberToChceck)
        self.assertNotEqual(defaultNumber, secondNumber)
    
    def testGetDefaultEmailOneEmail(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL))
        defaultNumber = phone.getDefaultEmail("firstName", "lastName")
        emailToChceck = phone.contacts[0].emails[0].email
        self.assertEqual(defaultNumber, emailToChceck)

    def testGetDefaultEmailTwoEmails(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL), Email("testmail@test2.com", EmailType.PERSONAL))
        defaultNumber = phone.getDefaultEmail("firstName", "lastName")
        emailToChceck = phone.contacts[0].emails[0].email
        secondEmail = phone.contacts[0].emails[1].email
        self.assertEqual(defaultNumber, emailToChceck)
        self.assertNotEqual(defaultNumber, secondEmail)
    
    def testChangeDefaultNumber(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Number("123456789", NumberType.HOME), Email("test_mail@gmail.com", EmailType.PERSONAL))
        defaultNumber = phone.getDefaultNumber("firstName", "lastName")
        numberToChceck = phone.contacts[0].numbers[0]
        secondNumber = phone.contacts[0].numbers[1]
        self.assertEqual(defaultNumber, numberToChceck)
        self.assertNotEqual(defaultNumber, secondNumber)
        lenBeforeChange = len(phone.contacts[0].numbers)
        phone.changeDefaultNumber("firstName", "lastName","123456789")
        defaultNumber = phone.getDefaultNumber("firstName", "lastName")
        self.assertEqual(defaultNumber, secondNumber)
        self.assertEqual(lenBeforeChange, len(phone.contacts[0].numbers))
        
    def testChangeDefaultEmail(self):
        phone = Contacts(self.__class__.contactFile)
        phone.addContact("firstName", "lastName", Number("890459632", NumberType.PERSONAL), Email("test_mail@gmail.com", EmailType.PERSONAL), Email("testmail@test2.com", EmailType.PERSONAL))
        defaultNumber = phone.getDefaultEmail("firstName", "lastName")
        emailToChceck = phone.contacts[0].emails[0].email
        secondEmail = phone.contacts[0].emails[1].email
        self.assertEqual(defaultNumber, emailToChceck)
        self.assertNotEqual(defaultNumber, secondEmail)
        phone.changeDefaultEmail("firstName", "lastName","testmail@test2.com")
        defaultEmail = phone.getDefaultEmail("firstName", "lastName")
        self.assertEqual(defaultEmail, secondEmail)
    
    def testContactGetItem(self):
        newNumber = Number("890459632", NumberType.PERSONAL)
        newEmail = Email("test_mail@gmail.com", EmailType.PERSONAL)
        contact = Contact("firstName", "lastName", [newNumber], [newEmail])
        contactFirstName = contact[0]
        self.assertEqual(contactFirstName, "firstName")
        contactLastName = contact[1]
        self.assertEqual(contactLastName, "lastName")
        contactNumber = contact[2][0].number
        self.assertEqual(contactNumber, newNumber.number)
        contactEmail = contact[3][0].email
        self.assertEqual(contactEmail, newEmail.email)

if __name__ == "__main__":
    unittest.main()