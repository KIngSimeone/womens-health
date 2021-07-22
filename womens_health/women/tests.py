from django.conf import settings
from django.test import Client, TestCase
from Users.models import Patient
from women.models import PeriodInfo, tests
from django.contrib.auth.hashers import make_password
import uuid

# Create your tests here.
client = Client()
secret = settings.ROOT_SECRET
content_type = "application/json"


class WomensTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        patient = Patient.objects.create(
            id=int(str(uuid.uuid4().int)[::6]),
            first_name='Atinuke',
            last_name='Okon',
            phone='07066782651',
            email='aitokon@gmail.com',
            password=make_password('Jehovah01'),
            birthday='1974-07-15'
        )
        patient.save()
        periodInfo = PeriodInfo.objects.create(
            id=int(str(uuid.uuid4().int)[::6]),
            patient=patient,
            cycle_average=25,
            period_average=5,
            last_period_date='2020-06-30',
            start_date='2020-05-25',
            end_date='2021-07-25'
        )
        periodInfo.save()

    def test_estimate_cycle(self):
        browser = Client()
        login_payload = {
            "userIdentity": "07066782651",
            "password": "Jehovah01",
        }
        estimate_payload = {
            "Last_period_date": "2020-06-30",
            "Cycle_average": 25,
            "Period_average": 5,
            "Start_date": "2020-05-25",
            "end_date": "2021-07-25"
        }
        login_response = browser.post(path="/v1/login", data=login_payload,
                                      content_type="application/json",
                                      HTTP_SECRET=settings.ROOT_SECRET, follow=True,
                                      secure=False, HTTP_ACCEPT='application/json', )

        estimate_response = browser.post(path="/v1/women/create-cycles", data=estimate_payload,
                                        follow=True, secure=False,
                                        HTTP_ACCEPT='application/json',
                                        content_type="application/json",
                                        HTTP_SECRET=settings.TEST_SECRET,
                                        HTTP_Token=login_response.json()['data'][
                                            'accessToken']
                                        )
        self.assertEqual(estimate_response.status_code, 200)
    
    def test_cycle_event(self):
        browser = Client()
        login_payload = {
            "userIdentity": "07066782651",
            "password": "Jehovah01",
        }
        login_response = browser.post(path="/v1/login", data=login_payload,
                                      content_type="application/json",
                                      HTTP_SECRET=settings.ROOT_SECRET, follow=True,
                                      secure=False, HTTP_ACCEPT='application/json', )

        event_response = browser.get(path="/v1/women/cycle-event?date=2020-07-25",
                                        follow=True, secure=False,
                                        HTTP_ACCEPT='application/json',
                                        content_type="application/json",
                                        HTTP_SECRET=settings.TEST_SECRET,
                                        HTTP_Token=login_response.json()['data'][
                                            'accessToken']
                                        )
        self.assertEqual(event_response.status_code, 200)
