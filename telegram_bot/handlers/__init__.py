from .admin_side import dp, bot
from .girls_side import dp, bot
from .main_menu import dp, bot

# is_unreg = await girlsclub_db.get_unregistered_girl(message.from_user.id)
#     if is_unreg is None:
from .helpers import get_id_from_message, create_keyboard_buttons
