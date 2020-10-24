#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 常量文件
# __date__: 2020/09/15 16

from enum import IntEnum, Enum
import os
from concurrent.futures import (ALL_COMPLETED, ThreadPoolExecutor,
                                as_completed, wait)
import multiprocessing
# 获取系统最大多线程数

MAX_CPUS = multiprocessing.cpu_count()//(1-0.9)
# LOG_DIR = os.path.join(current_floder, 'logs')


class DimTypeEnum(IntEnum):
    """
       0：表字段类型
       1：逻辑维度
       2：类型维度
       """
    # 表字段类型
    TABLE_FIELD = 0
    # 逻辑维度
    LOGIC_DIM = 1
    # 类型维度
    DIM_TYPE = 2

    @classmethod
    def value_str(cls, key):
        """
        使用字典的方式模拟switch语句
        """

        key_map = {
            cls.TABLE_FIELD.value: "表字段类型",
            cls.LOGIC_DIM.value: "逻辑维度",
            cls.DIM_TYPE.value: "类型维度",
        }

        return key_map.get(key, "")


class InputTypeEnum(IntEnum):
    """
       0：文本框；
       1：单选下拉框；
       2：定制
       """
    # 文本框
    TEXT_STR = 0
    # 单选下拉框
    SINGLE_PULL = 1
    # 定制
    CUSTOM = 2

    @classmethod
    def value_str(cls, key):
        """
        使用字典的方式模拟switch语句
        """

        key_map = {
            cls.TEXT_STR.value: "文本框",
            cls.SINGLE_PULL.value: "单选下拉框",
            cls.CUSTOM.value: "定制",
        }

        return key_map.get(key, "")


class PriorityConstant:
    """
    优先级
    """
    priority = 999999999

class IsActiveConstant:
    """
    是否删除
    """
    ACTIVE = True
    NO_ACTIVE = False
class IsDeletedConstant:
    """
    是否删除
    """
    DELETED = True
    NO_DELETED = False


class IsEnableConstant:
    """
    true：启用；false：禁用
    """
    ENABLE = True
    NO_ENABLE = False


class DataType(Enum):
    text = "text"
    checkbox = "checkbox"
    switch = "switch"
    multiButton = "multiButton"


class DisplayModeEnum(IntEnum):
    """
    字段展示模式
    0：展示name字段；
    1：展示name字段+code字段
   """
    # 展示name字段
    NAME = 0
    # 展示name字段+code字段
    NAME_AND_CODE = 1

    @classmethod
    def value_str(cls, key):
        """
        使用字典的方式模拟switch语句
        """

        key_map = {
            cls.NAME.value: "展示name字段",
            cls.NAME_AND_CODE.value: "展示name字段+code字段"
        }

        return key_map.get(key, "")


class ConstraintFieldTypeEnum(IntEnum):
    """
    约束项值类型（field_type 字段）
        0: 正整数
        1：非负整数
        2：布尔型
        3：正数
        4: object
        5: 日期

    为了添加新类型，需要：
    - 在 tools 中新建新类型的校验函数，
    - excel_validator.ColumnValueType 中也添加该类型，并创建继承 ValueValidatorBase 类创建用于的该类型导入时校验的子类。
    """
    # 0: 正整数
    POSITIVE_INTEGER = 0
    # 1：非负整数
    NON_NEGATIVE_INTEGER = 1
    # 2：布尔型
    BOOLEAN = 2
    # 3：正数
    POSITIVE_NUMBER = 3
    # 4：object
    OBJECT = 4
    # 5: 日期
    DATE = 5

    @classmethod
    def value_str(cls, key):
        """
        使用字典的方式模拟switch语句
        """

        key_map = {
            cls.POSITIVE_INTEGER.value: "正整数",
            cls.NON_NEGATIVE_INTEGER.value: "非负整数",
            cls.BOOLEAN.value: "布尔型",
            cls.POSITIVE_NUMBER.value: "正数",
            cls.OBJECT.value: "object",
            cls.DATE.value: "日期",
        }

        return key_map.get(key, "")

    @classmethod
    def type_hint(cls, key):
        """
        值类型的默认输入提示
        """
        key_map = {
            cls.POSITIVE_INTEGER.value: '请输入正整数',
            cls.NON_NEGATIVE_INTEGER.value: '请输入非负整数',
            cls.BOOLEAN.value: '请输入“是”或“否”',
            cls.POSITIVE_NUMBER.value: '请输入正数',
            cls.OBJECT.value: '',   # object类允许所有输入值，因此需要调用处自行处理
            cls.DATE.value: '请输入日期',
        }
        return key_map.get(key, "")


class DecisionTimeTypeEnum(Enum):
    """
    决策时间类型
    固定周期
    指定日期
    """
    # 固定周期
    FIXED_PERIOD = "固定周期"
    # 指定日期
    APPOINTED_DATE = "指定日期"

    @classmethod
    def value_str(cls, key):
        """
        使用字典的方式模拟switch语句
        """

        key_map = {
            cls.FIXED_PERIOD.value: "固定周期",
            cls.APPOINTED_DATE.value: "指定日期",
        }

        return key_map.get(key, "")


class DateConstants:
    """
    时间常量占位符
    """
    DATE_DATA = "9999-12-31"
