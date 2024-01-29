from dataclasses import dataclass
from rest_framework import serializers
from django.conf import settings
import django


@dataclass
class Person:
    name: str
    age: int


class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()


class ListPersonSerializer(serializers.Serializer):
    data = PersonSerializer(many=True)


class RetrievePersonSerializer(serializers.Serializer):
    data = PersonSerializer(source="*")



def serialize_response():
    person = Person(name="John", age=30)
    serializer = PersonSerializer(person)
    print(serializer.data)


def serialize_request():
    data = {
        "name": "John",
        "age": 30,
    }
    serializer = PersonSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)


def validate_request_data():
    data = {
        "name": "John",
    }
    serializer = PersonSerializer(data=data)
    serializer.is_valid(raise_exception=True)


def serialize_response_with_multiple_objects():
    people = {
        "data": [
            Person(name="John", age=30),
            Person(name="Jane", age=25),
        ]
    }
    serializer = ListPersonSerializer(people)
    print(serializer.data)


def serialize_response_with_single_nested_object():
    person = Person(name="John", age=30)
    serializer = RetrievePersonSerializer(person)
    print(serializer.data)


if __name__ == "__main__":
    settings.configure(DEBUG=True)
    django.setup()

    # serialize_response()
    # serialize_request()
    # validate_request_data()
    # serialize_response_with_multiple_objects()
    # serialize_response_with_single_nested_object()

