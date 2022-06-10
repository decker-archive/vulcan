# Manhattan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
import os
import threading
import time
import datetime


class SnowflakeFactory:
    def __init__(self) -> None:
        self._epoch: int = 1649325271415
        self._incrementation = 0

    def write(self) -> int:
        current_ms = int(time.time() * 1000)
        epoch = current_ms - self._epoch << 22

        epoch |= (threading.current_thread().ident % 32) << 17
        epoch |= (os.getpid() % 32) << 12

        epoch |= self._incrementation % 4096

        self._incrementation += 1

        return epoch

snowflake_factory = SnowflakeFactory()

if __name__ == '__main__':
    factory = SnowflakeFactory()
    print(factory.write())
    print(datetime.datetime.now(datetime.timezone.utc).isoformat())
