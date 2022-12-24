class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed  # средняя скорость, с которой двигался пользователь
        self.calories = calories  # количество килокалорий, которое израсходовал пользователь
        # за время тренировки

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{round(self.duration, 3)} ч.; '
                f'Дистанция:'
                f' {round(self.distance, 3)} км; Ср. скорость: '
                f'{round(self.speed, 3)} км/ч; Потрачено ккал: '
                f'{round(self.calories, 3)}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.6
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int, duration: float, weight: float) -> None:
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
        return InfoMessage('d', self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())

    def __str__(self):
        return f'{self.__class__.__name__}'


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() +
                 self.CALORIES_MEAN_SPEED_SHIFT) *
                self.weight / self.M_IN_KM * self.duration
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CONST_1 = 0.035
    CONST_2 = 0.029

    def __init__(self, height, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CONST_1 * self.weight + ((self.get_mean_speed() / 3600 * 1000) ** 2 /
                                               self.height)
                 * self.CONST_2 * self.weight) * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    INDEX = 1.1

    def __init__(self, length_pool, count_pool, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.INDEX) * 2 * self.weight * self.duration

    def __str__(self):
        return f'{self.__class__.__name__}'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_names = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    # swimming = Swimming()
    # return swimming
    return training_names[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = InfoMessage(training.show_training_info())
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        print(workout_type)
        print(data)

        training = read_package(workout_type, data)

        main(training)
