#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime


# controller 使用道德公共函数

# 设置创建时间及用户
async def set_create_datetime(target_obj, current_user):
    if hasattr(target_obj, 'create_by'):
        target_obj.create_by = current_user.user.user_name
    if hasattr(target_obj, 'create_time'):
        target_obj.create_time = datetime.now().replace(microsecond=0)
    if hasattr(target_obj, 'update_by'):
        target_obj.update_by = current_user.user.user_name
    if hasattr(target_obj, 'update_time'):
        target_obj.update_time = datetime.now().replace(microsecond=0)


# 设置更新时间及用户
async def set_update_datetime(target_obj, current_user):
    if hasattr(target_obj, 'update_by'):
        target_obj.update_by = current_user.user.user_name
    if hasattr(target_obj, 'update_time'):
        target_obj.update_time = datetime.now().replace(microsecond=0)
