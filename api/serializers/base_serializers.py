from rest_framework import serializers
from rest_framework.fields import empty
from api.common import constants, exceptions


class BaseSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=empty, tenant=None, tenant_user=None, user=None, extra_request=None, **kwargs):
        if extra_request is not None:
            if isinstance(data, list):
                for elem in data:
                    elem.update(extra_request)
            else:
                data.update(extra_request)

        super().__init__(instance=instance, data=data, **kwargs)
        self.tenant = tenant
        self.tenant_user = tenant_user
        self.user = user

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('created_at', 'updated_at', 'deleted_at')
        read_only_fields = ('id')
        extra_kwargs= {'created_by':{'write_only': True}, 'updated_by':{'write_only': True}}

    def __init__(self, instance=None, data=empty, tenant=None, tenant_user=None, user=None, extra_request=None, **kwargs):
        if extra_request is not None:
            if isinstance(data, list):
                for elem in data:
                    elem.update(extra_request)
            else:
                data.update(extra_request)
        super().__init__(instance=instance, data=data, **kwargs)
        self.tenant=tenant
        self.tenat_user=tenant_user
        self.user=user

    def create(self, validated_data):
        validated_data = self.creatorstamp(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self.updaterstamp(validated_data)
        return super().update(instance, validated_data)
    
    def _get_creator(self):
        creator= constants.BUILTIN_USER.SYSTEM.value
        if self.tenat_user is not None:
            creator = str(self.tenat_user.user.id)
        elif self.user is not None:
            creator = (constants.BUILTIN_USER.ANONYMOUS.value
                       if self.user.id is None else str(self.user.id))
        return creator
    
    def _get_updater(self):
        updater = constants.BUILTIN_USER.SYSTEM.value
        if self.tenat_user is not None:
            updater = str(self.tenat_user.user.id)
        elif self.user is not None:
            updater = (constants.BUILTIN_USER.ANONYMOUS.value
                       if self.user.id is None else str(self.user.id)) 
        return updater
    
    def creatorstamp(self, validated_date):
        creator = self._get_creator()
        validated_date['created_by'] = creator
        validated_date['updated_by'] = creator
        return validated_date
    
    def updaterstamp(self, validated_data):
        updater = self._get_updater()
        validated_data['updated_by'] = updater
        return validated_data
    
    def fill_missing_fields_by_instance(self, data):
        if self.instance is None:
            return data
        
        writable_fields = tuple(field.field_name for field in self._writable_fields)

        for field in writable_fields:
            if field not in data:
                data[field] = self.instance._meta.get_field(field).value_from_object(self.instance)
        return data
    
    def set_blank_explicitly(self, data, fields):
        for field in fields:
            if field not in data:
                continue
            if data[field] is None:
                data.pop(field)
            elif isinstance(data[field], str) and data[field] == '':
                data.pop(field)
            elif isinstance(data[field], list) and len(data[field]) == 0:
                data.pop(field)
            elif isinstance(data[field], dict) and len(data[field]) == 0:
                data.pop(field)
        return data
    
class DefaultListSerializer(serializers.ListSerializer):
    def validate(self, data):
        if len(data) > 20:
            raise exceptions.RequestSizeError('Request list size must be <= 20.')
        return super().validate(data)

class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=100)