from aiogram import F, Router, types


user_pr_router = Router()

@user_pr_router.message()
async def start_cmd(message: types.Message) -> None:
    await message.answer(message.text)