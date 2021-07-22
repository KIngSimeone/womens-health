# womens-health

A REST API that helps estimate a woman’s period cycles within a specific timeframe.

### What can you do
* Patients/Users/Women can sign up (Sign up is cumpolsory to use endpoints)
* Patients estimate their period cycles within a specific timeframe
* Patients can determine what period of her monthly cycle a lady is currently in.

### Sign Up
Sign up is neccesary on the platform.
For Security reasons users must have the secret key passed as `Secret` in their request headers to sign up, below is the current secret key

`LC9euClrULxcXghvIAf60VGkSESF6c5U7meVgD4tCEfGakZZH9l67eE7N2a3rFfi0IA6lpynEB0vajaSF8CeSKI3qGUoM2PAMYN780bmabzCESY2Dv3azFeV7suaY4S4cI0MyUxvPtQ97xYlbKxLkVaJ1N2fz2ghGWSwO2EnzPSoc7i3UIr5jATrVWuN90Ui3vO90FbQI4Kgce12GVns8zrWcM0PXHSdim8sSSiPWAvMJ904y2k5F3x93jpOVmR1`

Note: Secret key is also available in `.env` file for use

Below is the endpoint to sign up:
`localhost:8000/v1/users/patient`

Below is a sample sign up request body:
```
{
    "firstName": "Atinuke",
    "lastName": "Okon",
    "phone": "07066782651",
    "email": "aitokon@gmail.com",
    "password": "Jehovah01",
    "birthday": "1974-07-15"
}
```
After Sign up user can login to the platform with will return their access token in the response body. Please note `Secret` is also required in the request headers to login

Below is the log in endpoint:
`localhost:8000/v1/login`

Below is a sample request body, Users can use phone or email to login:
```
{
    "userIdentity": "aitokon@gmail.com",
    "password": "Jehovah01"
}
```

Below is the login response:
```
{
    "data": {
        "id": 1826014,
        "firstName": "Atinuke",
        "lastName": "Okon",
        "email": "aitokon@gmail.com",
        "phone": "07066782651",
        "address": null,
        "birthday": "1974-07-15",
        "accessToken": "ApEU4pTCULDVMi2z7ZQuK-euiMabYblCMF_20egT0J0"
    },
    "metaData": null,
    "message": "successfully authenticated"
}
```
**Please not you can login in with the credentials in the login request body, so u dont have to create a new user**

## Estimate Cycles

This endpoint will estimate the period cycles for the current logged in user/patient, for authentication user must pass the `accessToken` generated from thier login response in all other endpoints as `Token` in their request headers, this will also identify the current logged in user and retrieve their information

**Just a note `Token` is required in the request headers to use below endpoints.

Below is the endpoint to estimate cycles: `localhost:8000/v1/women/create-cycles`

Below is a sample request body:
```
{
  "Last_period_date":"2020-06-30",
  "Cycle_average":25,
  "Period_average":5,
  "Start_date":"2020-05-25",
  "end_date":"2021-07-25"
}
```

Below is sample response body:
```
{
    "data": {
        "total_created_cycles": 20
    },
    "metaData": null,
    "message": "success"
}
```