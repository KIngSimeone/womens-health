from datetime import datetime


def dateIsISO(value):
    try:
        # can validate 2019-03-04
        if value != str(datetime.strptime(value, "%Y-%m-%d").date()):
            raise ValueError
        return True
    except ValueError:
        return False
