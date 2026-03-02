# sms3.py Получение номера в вак смс
import time
import requests
import logging

# Глобальные переменные
tel = None
idNum = None
smsCode = None


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def send_get_request():
    global tel, idNum

    url = f"https://vak-sms.com/api/getNumber/?apiKey={apiKey}&service={service}&country={country}&operator={operator}"

    try:
        logging.info("Запрашиваем номер...")

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        tel = data.get("tel")
        idNum = data.get("idNum")

        if tel and idNum:
            logging.info(f"Номер получен: {tel}")
            logging.info(f"idNum: {idNum}")
            return True
        else:
            logging.error("Не удалось получить номер.")
            return False

    except Exception as e:
        logging.error(f"Ошибка запроса номера: {e}")
        return False


def send_get_request2(timeout_minutes=4):
    global smsCode, idNum

    if not idNum:
        logging.error("idNum отсутствует. Сначала получите номер.")
        return None

    end_time = time.time() + timeout_minutes * 60

    logging.info("Начинаем ожидание SMS...")

    while time.time() < end_time:

        url = f"https://vak-sms.com/api/getSmsCode/?apiKey={apiKey}&idNum={idNum}&all"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            smsCode = data.get("smsCode")

            if smsCode:
                logging.info(f"SMS код получен: {smsCode}")
                return smsCode

        except Exception as e:
            logging.error(f"Ошибка ожидания SMS: {e}")

        time.sleep(8)

    logging.warning("Время ожидания истекло.")
    return None


if __name__ == "__main__":
    if send_get_request():
        code = send_get_request2()

        print("SMS CODE:", code)
