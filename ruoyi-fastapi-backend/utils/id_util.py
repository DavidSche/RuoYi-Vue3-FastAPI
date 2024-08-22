#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import annotations
#
# from datetime import datetime
# from time import sleep
# from threading import (
#     Event,
#     Lock,
# )
# from typing import (
#     TYPE_CHECKING,
#     Generic,
#     TypeVar,
# )
#
# if TYPE_CHECKING:
#     from typing import (
#         Any,
#         Optional,
#         Tuple,
#         Type,
#     )
#
# __all__: Tuple[str, ...] = (
#     'SnowflakeGenerator',
# )
#
# _SnowflakeType = TypeVar(
#     '_SnowflakeType',
#     bound=int,
# )
#
# timestamp_bits: int = 2 ** 64
# process_id_bits: int = 2 ** 5
# thread_id_bits: int = 2 ** 5
# sequence_bits: int = 2 ** 12
# snowflake_bits: int = 2 ** 64
#
#
# class SnowflakeGenerator(Generic[_SnowflakeType]):
#     if TYPE_CHECKING:
#         _lock: Lock
#         _closed: Event
#         _epoch: datetime
#         _process_id: int
#         _thread_id: int
#         _step: int
#         _sequence: int
#         _last: datetime
#
#     def __init__(
#             self: SnowflakeGenerator,
#             epoch: datetime,
#             process_id: int,
#             thread_id: int,
#             step: int,
#             sequence: int,
#             last: datetime,
#     ) -> None:
#         self._lock = Lock()
#         self._closed = Event()
#
#         if not isinstance(epoch, datetime):
#             raise TypeError(f'Invalid epoch (object is not instance of datetime): {type(epoch).__name__}')
#
#         self._epoch = epoch
#
#         if process_id >= process_id_bits:
#             raise ValueError(
#                 f'Invalid process id value (process_id value greater than {process_id_bits - 1:,}): {process_id}')
#
#         self._process_id = process_id
#
#         if thread_id >= thread_id_bits:
#             raise ValueError(
#                 f'Invalid thread id value (thread_id value greater than {thread_id_bits - 1:,}): {thread_id}')
#
#         self._thread_id = thread_id
#
#         if step < 1:
#             raise ValueError(f'Invalid step value (step value less than 1): {step}')
#
#         if step >= sequence_bits:
#             raise ValueError(f'Invalid step value (step value greater than {sequence_bits - 1:,})): {step}')
#
#         self._step = step
#
#         if sequence >= sequence_bits:
#             raise ValueError(f'Invalid sequence (sequence value greater than {sequence_bits - 1:,}): {sequence}')
#
#         self._sequence = sequence
#
#         if last is None:
#             last = datetime.now()
#
#         if not isinstance(last, datetime):
#             raise TypeError(f'Invalid last (object is not instance of datetime): {type(last).__name__}')
#
#         self._last = last
#
#     @property
#     def epoch(self: SnowflakeGenerator) -> datetime:
#         return self._epoch
#
#     @property
#     def process_id(self: SnowflakeGenerator) -> int:
#         return self._process_id
#
#     @property
#     def thread_id(self: SnowflakeGenerator) -> int:
#         return self._thread_id
#
#     @property
#     def step(self: SnowflakeGenerator) -> int:
#         return self._step
#
#     @property
#     def sequence(self: SnowflakeGenerator) -> int:
#         return self._sequence
#
#     @sequence.setter
#     def sequence(
#             self: SnowflakeGenerator,
#             value: int,
#     ) -> None:
#         if self.closed:
#             raise RuntimeError(f'Cannot modify sequence value (snowflake generator is closed)')
#
#         if value >= sequence_bits:
#             raise ValueError(f'Invalid sequence (sequence value greater than {sequence_bits - 1:,}): {value}')
#
#         self._sequence = value
#
#     @property
#     def last(self: SnowflakeGenerator) -> datetime:
#         return self._last
#
#     @last.setter
#     def last(
#             self: SnowflakeGenerator,
#             value: datetime,
#     ) -> None:
#         if self.closed:
#             raise RuntimeError(f'Cannot modify last value (snowflake generator is closed)')
#
#         if not isinstance(value, datetime):
#             raise TypeError(f'Invalid last (object is not instance of datetime): {type(value).__name__}')
#
#         self._last = value
#
#     def __iter__(self: SnowflakeGenerator) -> SnowflakeGenerator:
#         return self
#
#     def __next__(self: SnowflakeGenerator) -> _SnowflakeType:
#         if self.closed:
#             raise StopIteration('Cannot get next snowflake (snowflake generator is closed)')
#
#         try:
#             return self.generate()
#         except (
#                 RuntimeError,
#                 ValueError,
#         ) as e:
#             raise StopIteration(f'Cannot get next snowflake ({e})')
#
#     def generate(self: SnowflakeGenerator) -> _SnowflakeType:
#         if self.closed:
#             raise RuntimeError(f'Cannot generate snowflake (snowflake generator is closed)')
#
#         self._lock.acquire()
#
#         now: datetime
#         sequence: int
#
#         while True:
#             now = datetime.now()
#
#             if self.last > now:
#                 sleep((self.last - now).total_seconds())
#                 continue
#
#             if self.last == now:
#                 sequence = (self.sequence + self.step) & (sequence_bits - 1)
#
#                 if sequence == 0:
#                     sleep(self.step / 1000)
#                     continue
#
#             else:
#                 sequence = 0
#
#             self.last = now
#             self.sequence = sequence
#
#             break
#
#         res = (
#                 (int(now.timestamp() * 1000) - int(self.epoch.timestamp() * 1000)) << 22 |
#                 self.process_id << 17 |
#                 self.thread_id << 12 |
#                 sequence
#         )
#
#         self._lock.release()
#
#         if res >= snowflake_bits:
#             raise ValueError(f'Invalid snowflake (snowflake value greater than {snowflake_bits - 1:,}): {res}')
#
#         return res
#
#     def close(self: SnowflakeGenerator) -> None:
#         self._closed.set()
#
#     @property
#     def closed(self: SnowflakeGenerator) -> bool:
#         return self._closed.is_set()

import time

# 项目元年时间戳
START_TIMESTAMP = 166666666666

# 机器ID bit位数
MACHINE_ID_BITS = 4

# 服务ID bit位数
SERVICE_ID_BITS = 3

# 序号 bit位数
SEQUENCE_BITS = 5

# 机器ID最大值计算
MAX_MACHINE_ID = (1 << MACHINE_ID_BITS) - 1

# 服务ID最大值计算
MAX_SERVICE_ID = (1 << SERVICE_ID_BITS) - 1

# 序号掩码最大值
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

# 移位偏移值计算
SERVICE_ID_SHIFT = SEQUENCE_BITS
MACHINE_ID_SHIFT = SEQUENCE_BITS + SERVICE_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + SERVICE_ID_BITS + MACHINE_ID_BITS


class SnowFlakeID:
    """
    用于生成IDs
    """

    def __init__(self, machine_id=1, service_id=1):
        """
        初始化
        :param machine_id: 机器ID
        :param service_id: 服务ID
        """
        # 校验机器ID
        if not (0 <= machine_id <= MAX_MACHINE_ID):
            raise ValueError('机器ID值越界')

        # 校验服务ID
        if not (0 <= service_id <= MAX_SERVICE_ID):
            raise ValueError('服务ID值越界')

        self.machine_id = machine_id
        self.service_id = service_id
        self.sequence = 0
        self.last_timestamp = -1  # 上次计算的时间戳

    @staticmethod
    def _gen_timestamp():
        """
        生成整数时间戳
        :return: int timestamp
        """
        return int(time.time() * 1000)

    @staticmethod
    def _til_next_millis(last_timestamp):
        """
        等到下一毫秒
        :param last_timestamp: 上次的时间戳
        :return: int
        """
        timestamp = SnowFlakeID._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = SnowFlakeID._gen_timestamp()
        return timestamp

    def generate_id(self):
        """
        生成ID
        :return: int
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨处理
        if (self.last_timestamp - timestamp) > 3:
            raise Exception('时钟回拨')
        if self.last_timestamp > timestamp:
            timestamp = self._til_next_millis(self.last_timestamp)

        # 如果是同一毫秒内生成的ID
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & MAX_SEQUENCE
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 核心ID生成逻辑
        gen_id = ((timestamp - START_TIMESTAMP) << TIMESTAMP_LEFT_SHIFT) | \
                 (self.machine_id << MACHINE_ID_SHIFT) | \
                 (self.service_id << SERVICE_ID_SHIFT) | \
                 self.sequence

        return gen_id

snowflake = SnowFlakeID(machine_id=1, service_id=2)


if __name__ == '__main__':

    start_timestamp = int(time.time() * 1000)
    for i in range(10):
        print(snowflake.generate_id())
    end_timestamp = int(time.time() * 1000)
    waste_time = (end_timestamp - start_timestamp) / 1000
    print(waste_time)