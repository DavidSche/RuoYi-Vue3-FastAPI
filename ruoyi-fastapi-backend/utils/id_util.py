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
MACHINE_ID_SHIFT = SERVICE_ID_SHIFT + SERVICE_ID_BITS
TIMESTAMP_LEFT_SHIFT = MACHINE_ID_SHIFT + MACHINE_ID_BITS


class SnowFlakeID:
    """
    用于生成唯一ID的类
    """

    def __init__(self, machine_id=1, service_id=1):
        if not (0 <= machine_id <= MAX_MACHINE_ID):
            raise ValueError(f"机器ID值越界，应在0到{MAX_MACHINE_ID}之间")

        if not (0 <= service_id <= MAX_SERVICE_ID):
            raise ValueError(f"服务ID值越界，应在0到{MAX_SERVICE_ID}之间")

        self.machine_id = machine_id
        self.service_id = service_id
        self.sequence = 0
        self.last_timestamp = -1  # 上次生成ID的时间戳

    @staticmethod
    def _gen_timestamp():
        """生成当前时间戳（毫秒）"""
        return int(time.time() * 1000)

    @staticmethod
    def _wait_for_next_millis(last_timestamp):
        """等待直到下一毫秒，以保证时间戳唯一性"""
        timestamp = SnowFlakeID._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = SnowFlakeID._gen_timestamp()
        return timestamp

    def generate_id(self):
        """生成唯一ID"""
        timestamp = SnowFlakeID._gen_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception('时钟回拨，拒绝生成ID')

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & MAX_SEQUENCE
            if self.sequence == 0:
                timestamp = SnowFlakeID._wait_for_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 生成ID，按顺序组合时间戳、机器ID、服务ID和序号
        gen_id = (
                ((timestamp - START_TIMESTAMP) << TIMESTAMP_LEFT_SHIFT) |
                (self.machine_id << MACHINE_ID_SHIFT) |
                (self.service_id << SERVICE_ID_SHIFT) |
                self.sequence
        )

        return gen_id


# 创建SnowFlakeID实例
snowflake = SnowFlakeID(machine_id=1, service_id=2)

# snowflake = SnowFlakeID(machine_id=1, service_id=2)

# 优化点：
# 提高可读性：
#
# 重命名 _til_next_millis 为 _wait_for_next_millis，更清晰地表达了该方法的功能。
# 错误消息中增加了具体的边界值提示，方便调试。
# 代码结构：
#
# 使用类级别的静态方法来生成时间戳，确保时间相关逻辑独立。
# 将ID生成的位操作整合在一起，减少代码冗余。
# 时间戳检查：
#
# 在ID生成过程中，检查当前时间戳是否小于上次生成的时间戳，防止时钟回拨导致的ID重复。
# 序列号循环：
#
# 使用按位与操作 (&) 限制序列号在最大值范围内自动循环，确保不会超出范围。
# 运行示例：
# 代码中包含了一个 if __name__ == "__main__": 块，方便在直接运行脚本时进行测试。你可以运行脚本来生成两个唯一的ID并输出到控制台。
# # 使用示例
if __name__ == '__main__':

    # 生成唯一ID
    unique_id = snowflake.generate_id()
    print(f"生成的唯一ID: {unique_id}")

    # 再次生成唯一ID
    another_unique_id = snowflake.generate_id()
    print(f"生成的另一个唯一ID: {another_unique_id}")

    start_timestamp = int(time.time() * 1000)
    for i in range(10):
        print(snowflake.generate_id())
    end_timestamp = int(time.time() * 1000)
    waste_time = (end_timestamp - start_timestamp) / 1000
    print(waste_time)
