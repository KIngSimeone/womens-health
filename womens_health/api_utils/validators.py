def validateKeys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys

def validateInputFormat(inputList, email, phone):
    if not validate_input_list_is_empty_and_clean(inputList):
        return False, f"Name can neither contain special characters nor be empty:{inputList}"

    if not validateEmailFormat(email):
        return False, f"Email format is invalid: {email}"

    if not validatePhoneFormat(phone):
        return False, f"Phone Format is Invalid: {phone}"

    return True, "success"