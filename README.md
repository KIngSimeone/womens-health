# womens-health

A REST API that helps estimate a woman’s period cycles within a specific timeframe.

### What can you do
* Patients/Users/Women can sign up (Sign up is cumpolsory to use endpoints)
* Patients estimate their period cycles within a specific timeframe
* Patients can determine what period of her monthly cycle a lady is currently in.

### Sign Up
Sign up is neccesary on the platform
For Security reasons users must have the secret key passed as `Secret` in their request headers to sign up, below is the current secret key and a sample as it is passed in as `Secret` in postman.

`LC9euClrULxcXghvIAf60VGkSESF6c5U7meVgD4tCEfGakZZH9l67eE7N2a3rFfi0IA6lpynEB0vajaSF8CeSKI3qGUoM2PAMYN780bmabzCESY2Dv3azFeV7suaY4S4cI0MyUxvPtQ97xYlbKxLkVaJ1N2fz2ghGWSwO2EnzPSoc7i3UIr5jATrVWuN90Ui3vO90FbQI4Kgce12GVns8zrWcM0PXHSdim8sSSiPWAvMJ904y2k5F3x93jpOVmR1`

Note: Secret key is also available in `.env` file for use