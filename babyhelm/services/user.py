from babyhelm.repositories.user import UserRepository


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, email: str, row_password: str):
        # TODO слой обращений к базе данных
        #  Проверить что такого пользователя еще нет по email
        #  Захэшировать пароль
        ...


