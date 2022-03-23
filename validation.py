import inquirer
import re 

def location_code_validation(answers,current):
    # length should be 3 and should be ascii
    flag = len(current)==3 and current.isascii()
    # If condition is not satisfied then
    if (not flag):
        raise inquirer.errors.ValidationError("", reason="Only 3 Letter location code should be given! \nSee https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm for Location Code")
    return True

def check_number(answers,current):
    if not current.isnumeric():
        raise inquirer.errors.ValidationError("", reason="Enter Integer value")
    return True

def date_validation(answers, current):
    if not re.match(r"(^(((0[1-9]|1[0-9]|2[0-8])[\/](0[1-9]|1[012]))|((29|30|31)[\/](0[13578]|1[02]))|((29|30)[\/](0[4,6,9]|11)))[\/](19|[2-9][0-9])\d\d$)|(^29[\/]02[\/](19|[2-9][0-9])(00|04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)$)", current):
        raise inquirer.errors.ValidationError("", reason="Invalid date format! Date format should be in DD/MM/YYYY")
    return True