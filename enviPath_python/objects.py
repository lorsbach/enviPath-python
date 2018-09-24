# -*- coding: utf-8 -*-
from enviPath_python.utils import Endpoint


class enviPathObject(object):
    """
    Base class for an enviPath object.
    """

    def __init__(self, requester, *args, **kwargs):
        """
        Constructor for any instance derived from enviPathObject.
        :param requester: The enviPathRequester used for getting this object.
        :param args: additional positional arguments.
        :param kwargs: additional named arguments. 'name' and 'id' are mandatory.
        """
        self.requester = requester
        # Make name optional to allow object creation with id only
        if kwargs['name']:
            self.name = kwargs['name']
        self.id = kwargs['id']
        self.loaded = False

    def get_type(self):
        """
        Gets the class name as string.
        :return: The class name as string. E.g. 'Package'
        """
        return type(self).__name__

    def __str__(self):
        """
        Simple string representation including type, name and id.
        :return: The object as string.
        """
        return '{}: {} ({})'.format(self.get_type(), self.name, self.id)

    def __repr__(self):
        """
        Same as __str__.
        :return: same as __str__.
        """
        return str(self)

    def _get(self, field):
        """
        Tries to get a field of the object. As objects are only initialized with 'name' and 'id' all other
        fields must be fetched from the enviPath instance. This fetches data only once.
        If the field is missing after getting the data from the enviPath instance an exception is risen.
        Should only be called by 'public' functions as they should implement appropriate object creation if value
        of requested field is an enviPathObject instance again.
        :param field: The field of interest.
        :return: The value of the field.
        """
        if not self.loaded and not hasattr(self, field):
            obj_fields = self._load()
            print(obj_fields)
            for k, v in obj_fields.items():
                setattr(self, k, v)

        if not hasattr(self, field):
            raise ValueError('{} has no property {}'.format(self.get_type(), field))

        return getattr(self, k)

    def _load(self):
        """
        Fetches data from the enviPath instance via the enviPathRequester provided at objects creation.
        :return: json containing the server response.
        """
        res = self.requester._get_request(self.id).json()
        return res

    def get_json(self):
        """
        Returns the objects plain JSON fetched from the instance.
        :return: A JSON object returned by the API.
        """
        return self.requester.get_json(self.id).json()


class Package(enviPathObject):
    def get_compounds(self):
        """
        Gets all compounds of the package.
        :return: List of Compound objects.
        """
        res = self.requester._get_objects(self.id + '/', Endpoint.COMPOUND)
        return res

    def get_rules(self):
        """
        Gets all rules of the package.
        :return: List of Rule objects.
        """
        res = self.requester._get_objects(self.id + '/', Endpoint.RULE)
        return res


class Compound(enviPathObject):
    pass


class Reaction(enviPathObject):
    pass


class Pathway(enviPathObject):
    pass


class Rule(enviPathObject):
    pass


class Scenario(enviPathObject):
    pass


class Setting(enviPathObject):
    pass


class User(enviPathObject):
    pass


class Group(enviPathObject):
    pass
