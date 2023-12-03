import aiohttp
import json
import csv


############################################################################################################
##                                                                                                        ##
##                                          POST METHODS                                                  ##
##                                                                                                        ##
############################################################################################################


async def send_to_api(endpoint, data=None, method='POST'):
    url = f'http://djangoapp:8000/api/{endpoint}'
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        if method == 'POST':
            async with session.post(url=url, data=json.dumps(data), headers=headers) as response:
                if response.status != 200:
                    # Handle error
                    response_data = await response.text()
                    print(f"Error: {response.status}. {response_data}")
                else:
                    return await response.json()
        elif method == 'DELETE':
            async with session.delete(url=url, headers=headers) as response:
                if response.status != 200:
                    # Handle error
                    response_data = await response.text()
                    print(f"Error: {response.status}. {response_data}")
                else:
                    return await response.json()


############################################################################################################
##                                                                                                        ##
##                                          GET METHODS                                                   ##
##                                                                                                        ##
############################################################################################################


async def get_from_api(endpoint, params=None):
    url = f'http://djangoapp:8000/api/{endpoint}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch data from API. Status: {response.status}")
                return None


############################################################################################################


# Для модели Event


async def create_event(name, price_for_new, price_for_old, event_photo_id, ticket_photo_id, description, event_date):
    data = {k: v for k, v in locals().items() if v is not None}
    return await send_to_api('event/create/', data)


async def update_event(name, new_name=None, new_price_for_new=None, new_price_for_old=None, new_event_photo_id=None, new_ticket_photo_id=None, new_description=None, new_event_date=None):
    data = {f'new_{k}': v for k, v in locals().items() if v is not None and k != 'name'}
    return await send_to_api(f'event/update/{name}/', data)


async def delete_event(name):
    return await send_to_api(f'event/delete/{name}/', method='DELETE')


async def get_event(name):
    return await get_from_api(f'event/get/{name}/')


# Для модели MemberGirl
async def create_member_girl(telegram_id, full_name, age, unique_id, discussion_topics, joining_purpose):
    data = {k: v for k, v in locals().items() if v is not None}
    return await send_to_api('member_girl/create/', data)


async def update_member_girl(telegram_id, new_full_name=None, new_age=None, new_discussion_topics=None, new_joining_purpose=None):
    data = {f'new_{k}': v for k, v in locals().items() if v is not None and k != 'unique_id'}
    return await send_to_api(f'member_girl/update/{telegram_id}/', data)


async def delete_member_girl(telegram_id):
    return await send_to_api(f'member_girl/delete/{telegram_id}/', method='DELETE')


async def get_member_girl(telegram_id):
    return await get_from_api(f'member_girl/get/{telegram_id}/')


async def get_all_members():
    return await get_from_api(f'member_girl/get_all/')


# Для модели Newsletter
async def create_or_update_newsletter(number=None, photo_id=None, text=None):
    data = {k: v for k, v in locals().items() if v is not None}
    return await send_to_api(f'newsletter/create_or_update/{number}/', data)


async def delete_newsletter(number):
    return await send_to_api(f'newsletter/delete/{number}/', method='DELETE')


async def get_newsletter(number):
    return await get_from_api(f'newsletter/get/{number}/')


async def create_unregistered_girl(telegram_id):
    data = {k: v for k, v in locals().items() if v is not None}
    return await send_to_api('member_girl/create/', data)


async def get_unregistered_girl(telegram_id):
    return await get_from_api(f'unregistered_girl/get/{telegram_id}/')


async def update_unregistered_girl(telegram_id):
    data = {f'new_{k}': v for k, v in locals().items() if v is not None and k != 'unique_id'}
    return await send_to_api(f'unregistered_girl/update/{telegram_id}/', data)
