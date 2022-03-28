from typing import Dict


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
        info_message = (InfoMessage(self.get_traning_type(), self.duration,
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

    def get_traning_type(self) -> str:
        return 'Running'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035
    K_2 = 0.029

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
                          * (self.duration * 60))
        return spent_calories

    def get_traning_type(self) -> str:
        return 'SportsWalking'


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

    def get_traning_type(self) -> str:
        return 'Swimming'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    package: Dict[str, Training] = {'SWM': Swimming,
                                    'RUN': Running,
                                    'WLK': SportsWalking
                                    }
    if workout_type not in package.keys():
        return 'Не определено'

    training_class = package.get(workout_type)
    training_object = training_class(*data)
    return training_object


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
