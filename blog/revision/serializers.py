from rest_framework import serializers
from rest_framework.exceptions import APIException
from reversion.models import Version
from reversion.errors import RevertError


class RevisionSerializer(serializers.ModelSerializer):
    version = serializers.PrimaryKeyRelatedField(read_only=True, source='id')
    updated_at = serializers.DateTimeField(read_only=True, source='revision.date_created')
    updated_by = serializers.PrimaryKeyRelatedField(read_only=True, source='revision.user')
    instance = serializers.JSONField(read_only=True, source='field_dict')

    class Meta:
        model = Version
        fields = ['version', 'updated_at', 'updated_by', 'instance']


class RevisionRevertSerializer(RevisionSerializer):

    def __init__(self, *args, **kwargs):
        super(RevisionSerializer, self).__init__(*args, **kwargs)
        version_queryset = self.context.get('versions')
        self.fields['version'] = serializers.PrimaryKeyRelatedField(write_only=True, queryset=version_queryset)

    def update(self, instance, validated_data):
        version = validated_data['version']
        try:
            version.revision.revert()
            return validated_data
        except RevertError:
            raise APIException(detail='can not revert instance.')

    class Meta(RevisionSerializer.Meta):
        fields = ['version']
