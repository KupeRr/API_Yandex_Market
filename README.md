# API_Yandex_Market
The program is designed to simplify work with the Yandex Market API. The main goal is to provide users with a simple and convenient interface for uploading pickup points of various campaigns to users' campaign profiles.

At the moment the program works with the following delivery services:
- CDEK
- Boxberry

The console interface is used for comfortable user experience.
In the next update is planned to add a graphical interface.

## Instructions for use

The following is required before using the program:
1. Create a business account in Yandex Market
2. Create a campaign
3. Create an application for the campaign and get the necessary accesses (https://yandex.ru/dev/market/partner-dsbs/doc/dg/concepts/authorization.html)
4. Get Boxberry API token

After the preparatory stage is passed it is necessary:
5. Download a copy of the project
```
git clone http://github.com/KupeRr/API_Yandex_Market
```
6. Rename the file **1.config** to **.config**
7. Insert the data you received at the preparation stage into the appropriate variables

Variables in the file ~~1.config~~ **.config**:
- *API_TOKEN_BOXBERRY* - The token to access the Boxberry API
- *API_OAUTH_ID_YANDEX* - Application number from OAuth to access Yandex API
- *API_OAUTH_TOKEN_YANDEX* - Application token from OAuth to access Yandex API
- *API_CAMPAIGN_ID_YANDEX* - The campaign number from the Yandex business profile. Note that the number starts after a dash. That is, if your profile says **12-345678**, the campaign number is **345678**.

----

After all of the above steps it is necessary to run the program by running a command in the directory where you downloaded a copy of the project
```
python main.py
```