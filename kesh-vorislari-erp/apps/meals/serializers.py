from rest_framework import serializers

from .models import Meal, Menu, MenuItem


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            "id",
            "name",
            "category",
            "description",
            "ingredients",
            "allergens",
            "portion",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = (
            "id",
            "meal",
            "category",
            "name",
            "description",
            "ingredients",
            "allergens",
            "portion",
            "notes",
            "sort_order",
        )


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)

    class Meta:
        model = Menu
        fields = ("id", "date", "notes", "created_by", "created_by_name", "items", "created_at", "updated_at")
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        menu = Menu.objects.create(created_by=self.context["request"].user, **validated_data)
        for item in items:
            MenuItem.objects.create(menu=menu, **item)
        return menu

    def update(self, instance, validated_data):
        items = validated_data.pop("items", None)
        instance.date = validated_data.get("date", instance.date)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        if items is not None:
            instance.items.all().delete()
            for item in items:
                MenuItem.objects.create(menu=instance, **item)
        return instance
