from datetime import timedelta


SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
'UPDATE_LAST_LOGIN': True,
}