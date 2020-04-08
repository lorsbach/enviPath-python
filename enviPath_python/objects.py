# -*- coding: utf-8 -*-
import json
from abc import ABCMeta
from io import BytesIO
from typing import List

from enviPath_python.enums import Endpoint, Model


class enviPathObject(metaclass=ABCMeta):
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
        if 'name' in kwargs:
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
        return '{}: {} ({})'.format(self.get_type(), self.get_name(), self.id)

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
            for k, v in obj_fields.items():
                setattr(self, k, v)
                self.loaded = True

        if not hasattr(self, field):
            raise ValueError('{} has no property {}'.format(self.get_type(), field))

        return getattr(self, field)

    def get_id(self):
        return self.id

    def __eq__(self, other):
        if type(other) is type(self):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def get_name(self):
        return self._get('name')

    def get_description(self):
        return self._get('description')

    def _load(self):
        """
        Fetches data from the enviPath instance via the enviPathRequester provided at objects creation.
        :return: json containing the server response.
        """
        res = self.requester.get_request(self.id).json()
        return res

    def get_json(self):
        """
        Returns the objects plain JSON fetched from the instance.
        :return: A JSON object returned by the API.
        """
        return self.requester.get_json(self.id).json()

    def _create_from_nested_json(self, member_name: str, nested_object_type):
        # TODO annotation for nested_type
        res = []
        plain_objs = self._get(member_name)
        for plain_obj in plain_objs:
            res.append(nested_object_type(self.requester, **plain_obj))
        return res

    def delete(self):
        """
        Deletes the object denoted by the internally maintained field `id`.
        :return:
        """
        if not hasattr(self, 'id') or self.id is None:
            raise ValueError("Unable to delete object due to missing id!")
        self.requester.delete_request(self.id)


class ReviewableEnviPathObject(enviPathObject, metaclass=ABCMeta):

    def get_review_status(self) -> str:
        return self._get('reviewStatus')

    def get_scenarios(self) -> List['Scenario']:
        res = []
        plain_scenarios = self._get('scenarios')
        for plain_scenario in plain_scenarios:
            res.append(Scenario(self.requester, **plain_scenario))
        return res


class Package(enviPathObject):

    def add_compound(self, smiles: str) -> 'Compound':
        pass

    def get_compounds(self) -> List['Compound']:
        """
        Gets all compounds of the package.
        :return: List of Compound objects.
        """
        res = self.requester.get_objects(self.id + '/', Endpoint.COMPOUND)
        return res

    def add_rule(self, smirks: str) -> 'Rule':
        pass

    def get_rules(self) -> List['Rule']:
        """
        Gets all rules of the package.
        :return: List of Rule objects.
        """
        res = self.requester.get_objects(self.id + '/', Endpoint.RULE)
        return res

    def add_reaction(self, name: str, description: str, educts: List['CompoundStructure'],
                     products: List['CompoundStructure']):
        pass

    def get_reactions(self) -> List['Reaction']:
        """
        Gets all reactions of the package.
        :return: List of Reaction objects.
        """
        res = self.requester.get_objects(self.id + '/', Endpoint.REACTION)
        return res

    def add_pathway(self):
        # TODO
        pass

    def predict(self, smiles, **kwargs):
        """
        Predicts a pathway.
        :param smiles: The SMILES string
        :param kwargs: possible additional parameters are:
                        'name' - the desired name for the pathway
                        'description' - the desired description for the pathway
                        'rootOnly' - 'true' or 'false', if set to 'true' a pathway only containing the root compound
                                      will be created. Default: 'false'
        :return: a Pathway object.
        """

        data = {
            'smilesinput': smiles
        }
        data.update(kwargs)
        res = self.requester.post_request(self.id + '/' + Endpoint.PATHWAY, params=None, payload=data).json()

        return Pathway(self.requester, **res)

    def get_pathways(self) -> List['Pathway']:
        """
        Gets all pathways of the package.
        :return: List of Pathway objects.
        """
        res = self.requester.get_objects(self.id + '/', Endpoint.PATHWAY)
        return res

    def add_relative_reasoning(self, name: str, packages: List['Package'], model: Model):
        # TODO
        pass

    def get_relative_reasonings(self) -> List['RelativeReasoning']:
        """
        Gets all relative reasonings of the packages.
        :return: List of RelativeReasoning objects.
        """
        res = self.requester.get_objects(self.id + '/', Endpoint.RELATIVEREASONING)
        return res

    def get_scenarios(self) -> List['Scenario']:
        """
        Gets all scenarios of the package.
        :return: List of Scenario objects.
        """
        res = self.requester.get_objects(self.id + '/', Endpoint.SCENARIO)
        return res

    def export_as_json(self) -> dict:
        params = {
            'exportAsJson': 'true',
        }
        raw_content = self.requester.get_request(self.id, params=params, stream=True).content
        buffer = BytesIO(raw_content)
        buffer.seek(0)
        return json.loads(buffer.read().decode())


# TODO aliases mixin


class Scenario(enviPathObject):
    pass


class Compound(ReviewableEnviPathObject):

    def get_structures(self) -> List['CompoundStructure']:
        """
        Gets all structures of this compound.
        :return: List of Structure objects.
        """
        res = []
        plain_structures = self._get('structures')
        for plain_structure in plain_structures:
            res.append(CompoundStructure(self.requester, **plain_structure))
        return res


class CompoundStructure(ReviewableEnviPathObject):

    def get_charge(self) -> float:
        return float(self._get('charge'))

    def get_formula(self) -> str:
        return self._get('formula')

    def get_mass(self):
        return self._get('mass')

    def get_svg(self) -> str:
        return self.requester.get_request(self._get('image')).text

    def is_default_structure(self):
        return self._get('isDefaultStructure')

    def get_smiles(self) -> str:
        return self._get('smiles')

    def get_inchi(self) -> str:
        return self._get('InChI')

    def get_halflifes(self) -> List[object]:
        return self._get('halflifes')


class Reaction(enviPathObject):

    def is_multistep(self) -> bool:
        return self._get('multistep')

    # TODO is this from Rule?
    def get_ec_numbers(self) -> List[object]:
        return self._get('ecNumbers')

    def get_smirks(self) -> str:
        return self._get('smirks')

    def get_pathways(self) -> List['Pathway']:
        return self._get('pathways')

    def get_medline_references(self) -> List[object]:
        return self._get('medlineRefs')

    def get_educts(self) -> List['CompoundStructure']:
        return self._create_from_nested_json('educts', CompoundStructure)

    def get_products(self):
        return self._create_from_nested_json('products', CompoundStructure)

    def get_rule(self) -> 'Rule':
        pass


class Rule(ReviewableEnviPathObject):

    def get_ec_numbers(self) -> List[object]:
        return self._get('ecNumbers')

    def included_in_composite_rule(self) -> List['Rule']:
        res = []
        for rule in self._get('includedInCompositeRule'):
            res.append(Rule(self, requester=self.requester, id=rule['id']))
        return res

    def is_composite_rule(self) -> bool:
        return self._get('isCompositeRule')

    def get_smirks(self) -> str:
        return self._get('smirks')

    def get_transformations(self) -> str:
        return self._get('transformations')

    def get_reactions(self) -> List['Reaction']:
        return self._create_from_nested_json('pathways', Reaction)

    def get_pathways(self) -> List['Pathway']:
        return self._create_from_nested_json('pathways', Pathway)

    def get_reactant_filter_smarts(self) -> str:
        return self._get('reactantFilterSmarts')

    def get_reactant_smarts(self) -> str:
        return self._get('reactantsSmarts')

    def get_product_filter_smarts(self) -> str:
        return self._get('productFilterSmarts')

    def get_product_smarts(self) -> str:
        return self._get('productsSmarts')

    def apply(self, compound):
        # TODO
        pass


class RelativeReasoning(ReviewableEnviPathObject):
    pass


class Node(enviPathObject):

    def get_compound(self):
        pass

    def get_depth(self) -> int:
        return self._get('depth')


class Edge(enviPathObject):
    # TODO add rule

    def get_start_nodes(self) -> List['Node']:
        return self._create_from_nested_json('startNodes', Node)

    def get_end_nodes(self) -> List['Node']:
        return self._create_from_nested_json('endNodes', Node)

    def get_reaction(self) -> Reaction:
        return Reaction(self.requester, id=self._get('reactionURI'))
        pass

    def get_reaction_name(self) -> str:
        return self._get('reactionName')

    def get_ec_numbers(self) -> List[object]:
        return self._get('ecNumbers')


class Pathway(enviPathObject):

    def get_nodes(self) -> List[Node]:
        return self._create_from_nested_json('nodes', Node)

    def get_edges(self) -> List[Edge]:
        return self._create_from_nested_json('links', Edge)

    def get_name(self) -> str:
        return self._get('pathwayName')

    def is_up_to_date(self) -> bool:
        return self._get('upToDate')

    def lastmodified(self) -> int:
        return self._get('lastModified')

    def is_completed(self) -> bool:
        return self._get('completed')


class Setting(enviPathObject):
    pass


class User(enviPathObject):
    pass


class Group(enviPathObject):
    pass
