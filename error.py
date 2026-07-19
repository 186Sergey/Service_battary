from datetime import datetime
import os


class Error:
    LOG_FILE = "errors_log.txt"
    """
    Класс централизованного логирования ошибок.
    Пишет ошибки в файл errors_log.txt с таймстепом.
    """
    @staticmethod
    def log(message: str):
        """
        Записывает сообщение об ошибке в файл errors_log.txt.
        :param message: Текст ошибки
        """
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        try:
            # Получаем абсолютный путь для ясности
            abs_path = os.path.abspath(Error.LOG_FILE)
            with open(Error.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
                print(f"[LOG] Ошибка записана в: {abs_path}")
        except Exception as e:
            fallback_msg = (
                f"[CRITICAL LOG FAIL] Не удалось записать ошибку в лог! "
                f"Путь: {os.path.abspath(Error.LOG_FILE)}, причина: {e}\n"
                f"Исходная ошибка, которую пытались залогировать: {message}"
            )
