import factory
from factory.django import DjangoModelFactory
from accounts.models import DefUser, Position, Department


class DepartmentFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Department {n}")

    class Meta:
        model = Department


class PositionFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Position {n}")
    department = factory.SubFactory(DepartmentFactory)

    class Meta:
        model = Position


class DefUserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"User1 {n}")
    first_name = factory.Sequence(lambda n: f"DefUser {n}")
    last_name = factory.Sequence(lambda n: f"DefUser {n}")
    position = factory.SubFactory(PositionFactory)
    signature = factory.django.ImageField(filename='signature.jpg')

    class Meta:
        model = DefUser


