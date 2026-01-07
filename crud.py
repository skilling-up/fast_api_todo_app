import aiosqlite
from database import DATABASE_URL,logger
async def add_user(name:str, age:int, email:str):
    async with aiosqlite.connect(DATABASE_URL) as db:
        try:
            insert_query = "INSERT INTO users (name,age,email) VALUES (?,?,?)"  
            cursor = await db.execute(insert_query, (name,age,email))
            await db.commit()
            return cursor.lastrowid
        except aiosqlite.IntegrityError:
            logger.info(f"Ошибка, пользователь с email:{email} уже существует")
# Асинхронная функция для получения всех пользователей
async def get_all_users():
    async with aiosqlite.connect(DATABASE_URL) as db:
        # Выполняем SELECT-запрос
        select_query = "SELECT id, name, age, email FROM users"

        # ВАЖНО: используем cursor для получения результата
        async with db.execute(select_query) as cursor:
            # fetchall() возвращает список кортежей
            rows = await cursor.fetchall()

        print("\n--- Список всех пользователей ---")
        for row in rows:
            user_id, user_name, user_age, user_email = row
            print(f"ID: {user_id}, Имя: {user_name}, Возраст: {user_age}, Email: {user_email}")
        print("-------------------------------\n")

        return rows



async def  update_user(user_id:int, new_name:str = None, new_age: int =None,new_email:str = None):
    async with aiosqlite.connect(DATABASE_URL) as db:
        update_data = {}
        if new_name is not None:
            update_data["name"] = new_name
        if new_age is not None:
            update_data["age"] = new_age
        if new_email is not None:
            update_data["email"] = new_email
         
        if not update_data:
            print(f"Нет данных для обновления пользователя с ID {user_id}.")
            return

        # Формируем строку SET динамически
        # Например, если нужно обновить name и age: "name = ?, age = ?"
        set_clause = ", ".join([f"{field} = ?" for field in update_data.keys()])

        # Полный SQL-запрос
        # Например: "UPDATE users SET name = ?, age = ? WHERE id = ?"
        sql_query = f"UPDATE users SET {set_clause} WHERE id = ?"

        # Подготовим список значений для плейсхолдеров
        # Сначала значения для SET, потом ID для WHERE
        values = list(update_data.values()) + [user_id]

        # Выполняем запрос
        await db.execute(sql_query, values)
        await db.commit()
        print(f"Пользователь с ID {user_id} обновлён. Обновлены поля: {list(update_data.keys())}")

       



async def delete_user(user_id:int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        delete_user = "DELETE FROM users WHERE id = ?"
        await db.execute(delete_user, (user_id,))
        await db.commit()
