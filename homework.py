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
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message

    def show_message(self) -> None:
        print(self.get_message())


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
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}')

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
    COEFF_KCAL_1 = 18
    COEFF_KCAL_2 = 20
    HOUR_TO_MIN = 60

    def get_spent_calories(self) -> float:
        upper_coeff = self.COEFF_KCAL_1 * self.get_mean_speed()
        avg_coeff = upper_coeff - self.COEFF_KCAL_2

        chunk = avg_coeff * self.weight

        return chunk / self.M_IN_KM * self.duration * self.HOUR_TO_MIN


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_KCAL_1 = 0.035
    COEFF_KCAL_2 = 0.029
    HOUR_TO_MIN = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        chunk_1 = self.get_mean_speed() ** 2 // self.height
        chunk_2 = self.COEFF_KCAL_1 * self.weight
        chunk_3 = self.COEFF_KCAL_2 * self.weight
        big_chunk = chunk_2 + chunk_1 * chunk_3

        return big_chunk * self.duration * self.HOUR_TO_MIN


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_KCAL_1 = 1.1
    COEFF_KCAL_2 = 2

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
        chunk = self.get_mean_speed() + self.COEFF_KCAL_1
        return chunk * self.COEFF_KCAL_2 * self.weight

    def get_mean_speed(self) -> float:
        for_readability = self.length_pool * self.count_pool
        return for_readability / self.M_IN_KM / self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}
    if workout_type not in trainings.keys():
        raise KeyError('Упс! Расчет для таких тренеровок еще не создан. '
                       'Доступные виды тренировок: '
                       f'{", ".join(list(trainings.keys()))}')
    else:
        return trainings[workout_type](*data)


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
