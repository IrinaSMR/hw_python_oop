from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

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
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % (self.__class__.__name__))

    def get_traning_type(self) -> str:
        return self.__class__.__name__

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = (InfoMessage(self.__class__.__name__, self.duration,
                        self.get_distance(), self.get_mean_speed(),
                        self.get_spent_calories()))
        return info_message


class Running(Training):
    """Тренировка: бег."""
    С_CAL_1 = 18
    C_CAL_2 = 20

    def get_spent_calories(self) -> float:
        spent_calories = ((self.С_CAL_1 * self.get_mean_speed()
                          - self.C_CAL_2) * self.weight / self.M_IN_KM
                          * (self.duration * 60))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035
    K_2 = 0.029
    MIN_IN_HOUR = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((self.K_1 * self.weight
                          + (self.get_mean_speed()**2 // self.height)
                          * self.K_2 * self.weight)
                          * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    K_3 = 1.1

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed = (self.length_pool
                      * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed() + self.K_3)
                          * 2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_type_classes: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                       'RUN': Running,
                                                       'WLK': SportsWalking
                                                       }
    if workout_type not in workout_type_classes:
        raise NotImplementedError('Неожидаемый тип {workout_type}')

    training_class: Type[Training] = workout_type_classes[workout_type]
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
