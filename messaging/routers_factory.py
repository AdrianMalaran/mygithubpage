# Python
# import new
import os
import sys


"""
This block incorrectly changes the system path.
It may also be redundant.
"""

# PROJECT_DIR = os.path.dirname(__file__)
# BASE_DIR = os.path.dirname(PROJECT_DIR)

# sys.path.append(PROJECT_DIR)
# sys.path.append(BASE_DIR)

# os.environ['PYTHONPATH'] = PROJECT_DIR
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


# Django
from django.conf import settings
# from django.db.models import get_models

# Package
# from rest_framework.pagination import PaginationSerializer
from rest_framework.routers import DefaultRouter

# Project
# from _base.serializers import BaseSerializer
# from _base.viewsets import BaseModelViewSet


class MasterRouter(DefaultRouter):
    def __init__(self, custom_modules, *args, **kwargs):
        super(MasterRouter, self).__init__(*args, **kwargs)

        #Only include the apps in the passed-in argument (string)
        self.our_apps = getattr(settings, custom_modules, None)
        if not self.our_apps:
            return

        #Automatically create the routers. This is where the magic happens.
        self._create_routers()

    def _is_mptt_field(self, field):
        mptt_fields = ['lft', 'rght', 'tree_id', 'level']
        for mf in mptt_fields:
            if field == mf:
                return True
        return False

    @classmethod
    def _is_module_exist(cls, package, module):
        import imp
        try:
            module_path = imp.find_module(package)[1]
            return os.path.isfile(os.path.join(module_path, module+".py"))
        except:
            return False

    @classmethod
    def MetaClassFactory(cls, arg_names):
        def __init__(self, **kwargs):
            for key , value in kwargs.items():
                if key not in arg_names:
                    raise TypeError("Argument %s not valid for %s"
                        % (key, self.__class__.__name__))
                setattr(self, key, value)
        meta_class = new.classobj("Meta", (), {})
        return meta_class

    @classmethod
    def ClassFactory(cls, name, arg_names, base_class):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                if key not in arg_names:
                    raise TypeError("Argument %s not valid for %s"
                        % (key, self.__class__.__name__))
                setattr(self, key, value)
            base_class.__init__(self)
        newclass = type(name, (base_class,),{})
        return newclass

    @classmethod
    #checks if the class is belong to us
    def is_class_exist(cls, package_name, module_name, class_name):
        if not cls._is_module_exist(package_name, module_name):
            return None

        import inspect
        module = getattr(__import__('.'.join((package_name, module_name))), module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if name == class_name:
                    return obj
        return None

    def _create_routers(self):
        for model in get_models():
            #Skip abstract models and those not in the apps to be REST'ified
            if not model._meta.abstract and model._meta.app_label in self.our_apps:

                package_name = model.__module__[:model.__module__.find('.')]

                #First, check if there is already a serializers.py file for that model
                serializer = self.is_class_exist(package_name, 'serializers', model.__name__+'Serializer')
                if not serializer:
                    # get all fields name except fields for model translation and django mptt
                    fields = ()
                    for f in model._meta.fields:
                        s_f = f.name
                        if self._is_mptt_field(s_f):
                            continue
                        fields += (s_f,)

                    # create Meta class for serializer
                    meta_class = self.MetaClassFactory(['model', 'fields'])
                    meta_class.model = model
                    meta_class.fields = fields

                    # create serializer
                    serializer = self.ClassFactory(model.__name__+'Serializer', ['Meta'], BaseSerializer)
                    serializer.Meta = meta_class
                    setattr(sys.modules[__name__], serializer.__name__, serializer)

                #Paginated serializer
                # paginated_serializer = self.is_class_exist(package_name, 'serializers', "Paginated"+model.__name__+'Serializer')
                # if not paginated_serializer:
                #     # create paginated serializer
                #     paginated_meta_class = self.MetaClassFactory(['object_serializer_class'])
                #     paginated_meta_class.object_serializer_class = serializer
                #     paginated_serializer = self.ClassFactory('Paginated'+model.__name__+'Serializer', ['Meta'], PaginationSerializer)
                #     paginated_serializer.Meta = paginated_meta_class
                #     setattr(sys.modules[__name__], paginated_serializer.__name__, paginated_serializer)

                #Checks for the standard syntax "ModelViewSet"
                view_set = self.is_class_exist(package_name, 'viewsets', model.__name__+'ViewSet')                
                if not view_set:
                    # create view set
                    view_set = self.ClassFactory(model.__name__+'ViewSet', ['queryset', 'serializer_class'], BaseModelViewSet)
                    view_set.queryset = model.objects.all()
                    view_set.serializer_class = serializer
                    setattr(sys.modules[__name__], view_set.__name__, view_set)
                else:
                    #print '\n\nFOUND CUSTOM VIEWSET!!!'
                    #print view_set
                    """
                    If there is customized viewset and there is not a customized serializer,
                    do not setup the serializer_class or set the serializer_class to None.
                    """
                    if not view_set.queryset:
                        view_set.queryset = model.objects.all()
                    if not view_set.serializer_class:
                        view_set.serializer_class = serializer

                setattr(self.__class__, serializer.__name__, serializer)
                # setattr(self.__class__, paginated_serializer.__name__, paginated_serializer)
                setattr(self.__class__, view_set.__name__, view_set)

                self.register(r'%s'%(model._meta.verbose_name_plural.lower().replace(' ', '-')),
                                view_set)

###### Test Code #######
# MasterRouter("OUR_MODULES")
# print MasterRouter.OrganizationSerializer
# from contact.models import Organization
# from _base.serializers import GroupSerializer
# OrganizationSerializer.add_or_set_field('groups', GroupSerializer(many=True))
# OrganizationSerializer.Set_opt('depth', 1)
# org_se = OrganizationSerializer(Organization.objects.all())
# org_se.add_or_set_field('groups', GroupSerializer(many=True))

# org_se.set_field('groups', GroupSerializer(many=True))
# org_se.set_opt('depth', 1)
# org_se.set_opt('depth', 0)

# for d in org_se.data:
#     print d
