import Logger
from SportsEquipment import *
from Customer import Customer 
from datetime import datetime
from Rental import Rental
from EquipmentFactory import EquipmentFactory
from Chain_of_Responsibilities import *
from RentalProcess import *

logger = Logger.logger

if __name__ == '__main__':
    handler = Operator(Manager(Admin()))
    
    eq1 = EquipmentFactory.create_equipment('bicycle', '1','some_bicycle', 'perfect', 100, 'Mountain')
    eq2 = EquipmentFactory.create_equipment('skis', '1', 'some_ski', 'good', 100, 170)
    eq3 = EquipmentFactory.create_equipment('tennisracket', '1', 'some_racket', 'good', 110, 1.2)

    proc1 = OnlineRentalProcess('1', Customer('1', "Boris"), eq1, datetime.now(), datetime.now() + timedelta(hours = 6), {"extra": 50})
    proc2 = OfflineRentalProcess('2', Customer('2', "Ramzan"), eq2, datetime.now(), datetime.now() + timedelta(hours = 6))
    proc3 = Rental('3', Customer('3', "Artem"), eq3, datetime.now(), datetime.now() + timedelta(hours = 3))

    print(eq1.log_action("some Action"))
    print(eq2.send_notification("Some note"))

    rent1 = proc1.rent_equipment(None)
    rent2 = proc2.rent_equipment(Request("easy", 150))
    print(rent1)
    print(rent2.to_dict())

    print(rent1.generate_report())

    print("Let`s check for error")
    
    try:
        proc4 = OnlineRentalProcess('4', Customer('4', "Rasim"), eq1, datetime.now(), datetime.now() + timedelta(hours = 1))
        rent4 = proc4.rent_equipment()
    except:
        print("Found exception")