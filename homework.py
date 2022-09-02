class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.round_with_zeros(self.duration)} ч.; '
                   f'Дистанция: {self.round_with_zeros(self.distance)} км; '
                   f'Ср. скорость: {self.round_with_zeros(self.speed)} км/ч; '
                   f'Потрачено ккал: {self.round_with_zeros(self.calories)}.')
        return message

    def show_message(self) -> None:
        print(self.get_message())

    def round_with_zeros(self, number: float) -> str:
        """Округление чисел с нулями после запятой."""
        number = round(number, 3)
        left_side = str(int(number))
        rigth_side = str(float(number) + 0.0001).split(".")[1][0:3]
        return f'{left_side}.{rigth_side}'


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_name = self.__class__.__name__
        return InfoMessage(training_name,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_kcal_1 = 18
        coeff_kcal_2 = 20

        avg_kcal_coeff = coeff_kcal_1 * self.get_mean_speed() - coeff_kcal_2

        return avg_kcal_coeff * self.weight / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029

        for_readability = (self.get_mean_speed() ** 2 // self.height)
        for_readability_2 = self.weight + for_readability * coeff_calorie_2
        for_readability_3 = (coeff_calorie_1 * for_readability_2 * self.weight)

        return for_readability_3 * self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        return (self.get_mean_speed() + coeff_calorie_1) * 2 * self.weight

    def get_mean_speed(self) -> float:
        for_readability = self.length_pool * self.count_pool
        return (for_readability / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    trainings = {'SWM': 'Swimming',
                 'RUN': 'Running',
                 'WLK': 'SportsWalking'}

    data = str(data).replace('[', '').replace(']', '')
    new_class = eval(trainings[workout_type] + f'({data})')

    return new_class


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info.show_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
