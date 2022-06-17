# Vulcan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
import datetime
import os
import threading
import time


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
