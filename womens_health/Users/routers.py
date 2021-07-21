from .views import provisionPatient
from errors.views import ErrorCodes
from api_utils.views import badRequestResponse, requestResponse


def patient_router(request):
    if request.method == 'POST':
        return provisionPatient(request)
    else:
        return requestResponse(badRequestResponse,
                               ErrorCodes.GENERIC_ERROR,
                               "Invalid Request method, Request Method must be 'POST'.")
