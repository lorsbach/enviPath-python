# -*- coding: utf-8 -*-

from enum import Enum


class Endpoint(Enum):
    USER = 'user'
    PACKAGE = 'package'
    COMPOUND = 'compound'
    PATHWAY = 'pathway'
    REACTION = 'reaction'
    RULE = 'rule'
    SCENARIO = 'scenario'
    SETTING = 'setting'
    GROUP = 'group'
    COMPOUNDSTRUCTURE = 'structure'
    NODE = 'node'
    EDGE = 'edge'
    RELATIVEREASONING = 'relative-reasoning'


class Model(Enum):
    RULEBASED = 'RULEBASED'
    ECC = 'ECC'
    MLCBMAD = 'MLCBMAD'
