from uuid import uuid4
from nicegui import ui

# ---------------- GLOBAL MESSAGE STORE ----------------
messages = []

# ---------------- CHAT MESSAGE LIST ----------------
@ui.refreshable
def chat_messages(own_id):
    for sender_id, avatar, text in messages:
        with ui.row().classes('w-full'):
            ui.chat_message(
                avatar=avatar,
                text=text,
                sent=(sender_id == own_id),
            ).classes('w-full')

# ---------------- MAIN PAGE ----------------
@ui.page('/')
def index():
    # ✅ user_id DEFINED HERE (PER USER SESSION)
    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    def send():
        if message_input.value.strip():
            messages.append((user_id, avatar, message_input.value))
            chat_messages.refresh()
            message_input.value = ''

    # ---------- MESSAGE AREA ----------
    with ui.column().classes('w-full h-screen'):
        with ui.column().classes('flex-grow overflow-auto w-full p-4'):
            chat_messages(user_id)   # ✅ user_id exists here

    # ---------- FOOTER ----------
    with ui.footer().classes('bg-white p-3 shadow-lg'):
        with ui.row().classes('w-full items-center gap-3'):
            with ui.avatar():
                ui.image(avatar)

            message_input = (
                ui.input(placeholder='Type a message...')
                .props('rounded outlined')
                .classes('flex-grow')
                .on('keydown.enter', send)
            )

            ui.button('Send', on_click=send)

# ---------------- RUN SERVER ----------------
ui.run()
