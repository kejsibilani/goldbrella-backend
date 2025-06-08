import os

system_info = dict(
    name=os.getenv('COMPANY_NAME'),
    logo=os.getenv('COMPANY_LOGO'),
    email=os.getenv('COMPANY_EMAIL'),
    website=os.getenv('COMPANY_WEBSITE'),
    phone_number=os.getenv('COMPANY_PHONE_NUMBER'),
    owner_first_name=os.getenv('COMPANY_OWNER_FIRST_NAME'),
    owner_last_name=os.getenv('COMPANY_OWNER_LAST_NAME')
)
