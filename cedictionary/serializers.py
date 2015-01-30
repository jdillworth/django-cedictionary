from rest_framework import serializers

from . import models

class DefinitionField(serializers.RelatedField):
    def to_representation(self, value):
        return value.definition

class ChineseEntrySerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionField(read_only=True, many=True)

    class Meta:
        model = models.ChineseEntry
        read_only_fields = fields = ('url',
            'ch', 'chs', 'pinyin', 'pinyin_tone_marked',
            'pinyin_letters', 'definitions')
