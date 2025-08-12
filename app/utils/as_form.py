
from typing import get_type_hints
from fastapi import Form
from sqlalchemy import inspect


def as_form(cls):
    """
    Декоратор, чтобы Pydantic-модель можно было принимать через multipart/form-data
    """
    new_params = []
    type_hints = get_type_hints(cls)
    
    for name, model_field in cls.model_fields.items():
        field_type = type_hints.get(name, str)

        if model_field.is_required():
            default = Form(...)
        else:
            default = Form(model_field.default)

        param = inspect.Parameter(
            name,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default,
            annotation=field_type,
        )
        new_params.append(param)

    cls.__signature__ = inspect.signature(cls).replace(parameters=new_params)
    return cls
