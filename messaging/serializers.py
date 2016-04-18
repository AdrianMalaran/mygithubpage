from rest_framework import serializers
from .models import *

class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        depth = kwargs.pop('depth', None)

        super(BaseSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        # Replace the default DateTimeField to BaseDateTimeField
        for k, v in self.fields.iteritems():
            if isinstance(v, serializers.DateTimeField):
                self.fields[k] = BaseDateTimeField()

        if depth:
            self.set_opt('depth', depth)

    @classmethod
    def get_default_fields_name(cls):
        fields = ()
        for f in cls.Meta.model._meta.fields:
            fields += (f.name,)

        return fields

    def set_field(self, name, value=None):
        opt_fields = self.fields.keys()

        fields = {}

        if isinstance(name, str):
            fields[name] = value
        elif hasattr(name, '__iter__'):
            fields = name
        else:
            raise Exception("Name should be str or dict, %s is given."%(type(name)))

        if not isinstance(fields, dict):
            for f in fields:
                if not isinstance(f, str):
                    raise Exception("Field name should be str, %s is given."%(type(f)))
                if not f in opt_fields:
                    opt_fields += (f,)
        else:
            for fn, fv in fields.iteritems():
                if not isinstance(fn, str):
                    raise Exception("Field name should be str, %s is given."%(type(fn)))
                if not fn in opt_fields:
                    opt_fields += (fn,)
                # If there is a customized value given for the field, add it to
                # the base_fields.
                if fv and fn not in self.base_fields:
                    self.base_fields[fn] = fv

        self.opts.fields = opt_fields

        self.fields = self.get_fields()
        if isinstance(fields, dict):
            for fn, fv in fields.iteritems():
                if fn and fv:
                    self.fields[fn] = fv

        return True

    def remove_field(self, name):
        fields = []

        if isinstance(name, str):
            fields.append(name)
        elif hasattr(name, '__iter__'):
            fields = name
        else:
            raise Exception("name should be str or iterable, %s is given."%(type(name)))

        for f in fields:
            l_fields = list(self.opts.fields)
            if f in l_fields:
                l_fields.remove(f)
                self.opts.fields = tuple(l_fields)

            if self.base_fields.has_key(f):
                del self.base_fields[f]
        self.fields = self.get_fields()
        for f in fields:
            if self.fields.has_key(f):
                del self.fields[f]

        self.opts.fields = tuple(self.fields.keys())

        return True

    def set_opt(self, name, value):
        if not isinstance(name, str):
            return False

        setattr(self.opts, name, value)

        self.fields = self.get_fields()

    def set_depth(self, depth):
        self.set_opt('depth', depth)

    @classmethod    # set or add fields globally
    def Add_or_set_field(cls, field_name, filed_value=None):
        fields = {}

        if isinstance(field_name, str):
            fields[field_name] = filed_value
        elif hasattr(field_name, '__iter__'):
            fields = field_name
        else:
            raise Exception("field_name should be str or iterable, %s is given."%(type(field_name)))

        # If fields is not defined in Meta class, add it and assign default
        # fields to it.
        if not hasattr(cls.Meta, 'fields'):
            setattr(cls.Meta, "fields", cls.get_default_fields_name())

        if isinstance(fields, dict):
            new_fields = set(fields.keys()) - set(cls.Meta.fields)
        else:
            new_fields = set(fields) - set(cls.Meta.fields)
        cls.Meta.fields += tuple(new_fields)

        if isinstance(fields, dict):
            for f, v in fields.iteritems():
                if v:
                    cls.base_fields[f] = v
        elif isinstance(field_name, str) and filed_value:
            cls.base_fields[field_name] = filed_value

        return True

    @classmethod
    def Remove_field(cls, field_name):
        fields = []
        if isinstance(field_name, str):
            fields.append(field_name)
        elif hasattr(field_name, '__iter__'):
            fields = field_name
        else:
            raise Exception("field_name should be str or iterable, %s is given."%(type(field_name)))

        # If fields is not defined in Meta class, add it and assign default
        # fields to it.
        if not hasattr(cls.Meta, 'fields'):
            setattr(cls.Meta, "fields", cls.get_default_fields_name())

        declared = list(cls.Meta.fields)
        for f in fields:
            if f in declared:
                declared.remove(f)
            else:
                raise Exception("field is not exist, %s is given." % (str(f)))

        cls.Meta.fields = tuple(declared)

        return True

    @classmethod
    def Set_opt(cls, opt_name, opt_value):
        if not isinstance(opt_name, str):
            return False
        if not hasattr(cls, 'Meta'):
            return False

        setattr(cls.Meta, opt_name, opt_value)

        return True

    @classmethod
    def Remove_opt(cls, opt_name):
        if not isinstance(opt_name, str):
            return False
        if not hasattr(cls, 'Meta'):
            return False

        delattr(cls.Meta, opt_name)

        return True

    def gfk_objs(self, model_class, obj):
        ct = ContentType.objects.get_for_model(obj)
        objs = model_class.objects.filter(content_type=ct, object_id=obj.id)

        return objs

    def get_serialized_objs(self, model_class, model_serializer, obj,
                            order_by=None):
        objs = self.gfk_objs(model_class, obj)
        if order_by:
            objs.order_by(order_by)

        return model_serializer(objs, many=True).data

class ContactSerializer(BaseSerializer):
	
	class Meta:
		model = Contact
		fields = ('id', 'first_name', 'last_name', 'phone_number',)

class MessageSerializer(BaseSerializer):

	class Meta:
		model = Message
		fields = ('id', 'text', 'contact','sent_by_me',)