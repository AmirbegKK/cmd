# ai-charity-assist

Бот поддержки для благотворительных сервисов.

Бот принимает отзывы, отвечает на частые вопросы и даёт рекомендации 
по проектам.

# Установка

    pip install --upgrade pip
    pip install pyenv
    pyenv install 3.12
    pyenv virualenv 3.12 assist-bot
    pyenv local assist-bot
    pip install -r requirements.txt

# Заполнение БД
Файл base.py - отвечает за перенос данных из excel в бд (особо не вникайте, сделано для удобства и асинхронной работы)

Создайте папку datasets и поместите туда файл campaigns.xlsx.
Затем запустите base.py через 

    python base.py

и ваша база данных готова.

# Запуск
    python start.py
Тег бота - https://t.me/toobahack_bot
