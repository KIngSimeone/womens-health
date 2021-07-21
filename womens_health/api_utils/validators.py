import re
from data_transformer.views import stringIsInteger


def validateThatStringIsEmptyAndClean(value):
    is_clean = (re.compile(r'[@_!#$%^&*()<>?/\|}{~:]').search(value) is None)
    not_empty = (len(value.strip()) != 0)
    return (is_clean and not_empty)


def validateEmailFormat(email):
    emailPattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

    if(re.search(emailPattern, email)):
        return True
    return False


def validatePhoneFormat(phone):
    if not stringIsInteger(phone):
        return False
    else:
        return True


def validateKeys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys


def validate_input_list_is_empty_and_clean(inputList):

    for item in inputList:
        if validateThatStringIsEmptyAndClean(item):
            return True


def validateInputFormat(inputList, email, phone):
    if not validate_input_list_is_empty_and_clean(inputList):
        return False, f"Name can neither contain special characters nor be empty:{inputList}"

    if not validateEmailFormat(email):
        return False, f"Email format is invalid: {email}"

    if not validatePhoneFormat(phone):
        return False, f"Phone Format is Invalid: {phone}"

    return True, "success"
