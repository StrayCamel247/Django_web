import wsme
from wsme import types as wtypes
from apps import types as _types
from django.utils.translation import gettext_lazy as _
from apps.api_exception import ParameterException
from .handler import KpiFactory


class InterfaceResult(_types.SuccessResult):
    pass


