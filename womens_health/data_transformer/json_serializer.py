from .views import toUiReadableDateFormat


def transformPatient(patient):
    return {
        'id': patient.id,
        'firstName': patient.first_name,
        'lastName': patient.last_name,
        'email': patient.email,
        'phone': patient.phone,
        'address': patient.address,
        'birthday': patient.birthday,
        'createdAt': toUiReadableDateFormat(patient.created_at),
        'updatedAt': toUiReadableDateFormat(patient.updated_at)
    }

def userLoginResponse(user, access_token):
    return {
        'id': user.id,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
        'birthday': user.birthday,
        'accessToken': access_token
    }