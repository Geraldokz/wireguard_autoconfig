from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

from mainapp.exceptions import ModelDeleteException


def delete_model_object(object_id: int, model: Type[Model]) -> None:
    """Delete model object by id"""
    model_object = _get_model_object(object_id, model)
    model_object.delete()


def _get_model_object(object_id: int, model: Type[Model]) -> Model:
    """Find model object by id"""
    try:
        model_object = model.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        raise ModelDeleteException(f'vpn server with id {object_id} does not exist')
    return model_object
