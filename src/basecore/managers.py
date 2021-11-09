from django.db import models
from django.db.models import QuerySet


class QuerySetDelete(models.query.QuerySet):

    def delete(self) -> None:
        self.update(is_alive=False)

    def get_queryset(self) -> QuerySet:
        return self.filter(is_alive=True)


class BaseModelManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return QuerySetDelete(self.model).get_queryset()
