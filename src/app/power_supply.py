"""Управление источниками питания."""

import asyncio
import json
import logging
import os
import socket

from dotenv import load_dotenv

load_dotenv()
POWER_SUPPLY_HOST = os.getenv("POWER_SUPPLY_HOST")
POWER_SUPPLY_PORT = os.getenv("POWER_SUPPLY_PORT")

logging.basicConfig(filename='power_supply.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class PowerSupply:
    """Взаимодействие с источниками питания."""

    def __init__(self, host=POWER_SUPPLY_HOST, port=POWER_SUPPLY_PORT):
        self.host = host
        self.port = port
        self.connection = None

    async def is_connected(self):
        return self.connection is not None

    async def connect(self):
        """Подключение к сервису."""
        
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.host, self.port))
        except Exception as e:
            await self.disconnect()
            logging.error(f"Failed to connect to the power supply: {e}")
            raise Exception("Failed to connect to the power supply")

    async def disconnect(self):
        """Отключение от сервиса."""

        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            logging.error(f"Error while disconnecting from the power supply: {e}")

    async def send_command(self, command):
        """Отправка комманды."""

        try:
            if self.connection:
                self.connection.send(command.encode())
        except Exception as e:
            logging.error(f"Error while sending command to the power supply: {e}")

    async def receive_response(self):
        """Получение ответа."""

        try:
            if self.connection:
                response = self.connection.recv(1024)
                return response.decode()
        except Exception as e:
            logging.error(f"Error while receiving response from the power supply: {e}")

    async def set_channel_current(self, channel, current):
        """Установить ток каналу питания."""

        try:
            await self.send_command(f":MEASure{channel}:CURRent {current}\n")
        except Exception as e:
            logging.error(f"Error while setting current for channel {channel}: {e}")
            raise Exception(f"Failed to set current for channel {channel}")

    async def set_channel_voltage(self, channel, voltage):
        """Установить напряжения каналу питания."""

        try:
            await self.send_command(f":MEASure{channel}:VOLTage {voltage}\n")
        except Exception as e:
            logging.error(f"Error while setting voltage for channel {channel}: {e}")

    async def enable_channel_output(self, channel):
        """Включить выход канала питания."""

        try:
            await self.send_command(f":OUTPut{channel}:STATe 1\n")
        except Exception as e:
            logging.exception(f"Error while enabling output for channel {channel}: {e}")

    async def disable_channel_output(self, channel):
        """Выключить выход канала питания."""

        try:
            await self.send_command(f":OUTPut{channel}:STATe 0\n")
        except Exception as e:
            logging.exception(f"Error while disabling output for channel {channel}: {e}")

    async def query_voltage(self, channel):
        """Получить напряжение канала питания."""

        try:
            await self.send_command(f":MEASure{channel}:VOLTage?\n")
            response = float(await self.receive_response())
            return response
        except Exception as e:
            logging.error(f"Error while querying voltage for channel {channel}: {e}")


    async def query_current(self, channel):
        """Получить ток канала питания."""

        try:
            await self.send_command(f":MEASure{channel}:CURRent?\n")
            response = float(await self.receive_response())
            return response
        except Exception as e:
            logging.error(f"Error while querying current for channel {channel}: {e}")

    async def query_power(self, channel):
        """Получить мощность канала питания."""

        try:
            await self.send_command(f":MEASure{channel}:POWEr?\n")
            response = float(await self.receive_response())
            return response
        except Exception as e:
            logging.error(f"Error while querying power for channel {channel}: {e}")

    async def query_all_channel_status(self):
        """Получить данные по всем источника питания."""

        try:
            command = ":MEASure1:ALL?,MEASure2:ALL?,MEASure3:ALL?,MEASure4:ALL?\n"
            await self.send_command(command)
            response = await self.receive_response()

            # Парсинг ответа и формирование данных в формате JSON
            parsed_data = {}
            channel_data = response.split(',')
            num_channels = len(channel_data) // 3

            for i in range(num_channels):
                channel_number = int(channel_data[i * 3])
                status = channel_data[i * 3 + 1]
                current = float(channel_data[i * 3 + 2])

                parsed_data[f"channel_{channel_number}"] = {
                    "status": status,
                    "current": current
                }

            return json.dumps(parsed_data)
        except Exception as e:
            logging.error(f"Error while querying all channel status: {e}")

    async def poll_telemetry(self, interval=10):
        """Получить телеметрию каналов питания."""

        while True:
            try:
                telemetry_data = await self.query_all_channel_status()
                logging.info(f"Telemetry data: {telemetry_data}")
                await asyncio.sleep(interval)
            except Exception as e:
                logging.error(f"Telemetry polling error: {str(e)}")
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()


    async def main():
        power_supply = PowerSupply(host="", port="")
        await power_supply.connect()

        await power_supply.set_channel_current(1, 5)
        await power_supply.set_channel_current(1, 3)

        status = await power_supply.query_all_channel_status()
        print(status)

        await power_supply.disconnect()


    loop.run_until_complete(main())