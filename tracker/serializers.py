from tracker.models import Addiction, Periodicity, NiceAddiction
from rest_framework import serializers

from tracker.validators import RunTimeValidation


class PeriodicitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода периодичности
    """

    class Meta:
        model = Periodicity
        fields = '__all__'


class NiceAddictionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода приятной привычки
    """

    class Meta:
        model = NiceAddiction
        fields = '__all__'


class AddictionSerializer(serializers.ModelSerializer):
    """
    Для создания привычки требуется передавать в полях periodicity_data и nice_addiction_data словарь -
    содержащий в себе данные для создания этих объектов, пример ниже:
    {
    "location": "Каэр МоргенШтерн",
    "time": "18.00",
    "activity_name": "Готовить зелье из накера",
    "nice_addiction_data": {
        "location": "Каэр морхен",
        "time": "20.00",
        "activity_name": "Подшутить над дядькой Весемиром"

    },
    "periodicity": {
            "on_Monday": false,
            "on_Tuesday": false,
            "on_Wednesday": true,
            "on_Thursday": false,
            "on_Friday": false,
            "on_Saturday": false,
            "on_Sunday": true
    },
    // "prize": "Кружка пива",
    "run_time": "300",
    "is_public": true

    }
    """
    periodicity_data = PeriodicitySerializer(source='periodicity', many=False,
                                             read_only=True)
    # для преодоления конфликтов данные по переодичности
    # и приятной привычке выводятся отдельно
    nice_addiction_data = NiceAddictionSerializer(source='nice_addiction', many=False, read_only=True)
    validators = [
        RunTimeValidation(field='run_time'),
    ]

    class Meta:
        model = Addiction
        # fields = '__all__'
        exclude = ('periodicity', 'nice_addiction')

    def create(self, validated_data):
        """
        Для создания объектов был переопределен метод create
        Он же является и неким валидатором данных
        :param validated_data:
        :return:
        """
        if 'nice_addiction_data' and 'prize' in validated_data:
            # выбрасывает ошибку если одновременно заполнены оба поля
            raise serializers.ValidationError('Необходимо выбрать что то одно')
        if 'nice_addiction_data' in self.context['request'].data:
            """
            Если были переданы данные для приятной привычки то словарь распаковывается и создает новый объект
            Ссылка на него добавляется в словарь validated_data
            """
            try:
                nice_addiction = NiceAddiction.objects.create(**self.context['request'].data['nice_addiction_data'])
                nice_addiction.save()
                validated_data['nice_addiction'] = nice_addiction
            except KeyError:
                raise serializers.ValidationError('Необходимо правильно заполнить поля nice_addiction_data')
        else:
            if 'prize' not in validated_data:
                # если не оказалось и поля prize - то выбрасывает ошибку
                raise serializers.ValidationError('Необходимо заполнить поля nice_addiction_data или prize')
        try:
            if True not in self.context['request'].data['periodicity'].values():
                # если все поля в словаре для периодичности содержат false, то выбрасывает ошибку
                # если все ок, создает и сохраняет объект, добавляет его в словарь validated_data
                raise serializers.ValidationError('Необходимо выбрать хотя бы один день недели')
            periodicity = Periodicity.objects.create(**self.context['request'].data["periodicity"])
            periodicity.save()
            validated_data['periodicity'] = periodicity
        except KeyError:
            # если переданный словарь неправильно заполнен, выкидывает ошибку
            raise serializers.ValidationError('Необходимо правильно заполнить поля periodicity')

        validated_data['proprietor'] = self.context['request'].user  # добавляет пользователя в validated_data

        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance
