Install using ``pip``…

::

    pip install -e git+https://github.com/lorsbach/enviPath-python#egg=enviPath-python
    
Quickstart…
::

    from enviPath_python.enviPath import *
    from enviPath_python.objects import *
    from time import sleep

    # Define the instance to use
    INSTANCE_HOST = 'https://envipath.org/'
    EAWAG_BBD = '{}package/32de3cf4-e3e6-4168-956e-32fa5ddb0ce1'.format(INSTANCE_HOST)
    ANONYMOUS_PACKAGE = '{}package/650babc9-9d68-4b73-9332-11972ca26f7b'.format(INSTANCE_HOST)

    # Each journey starts with setting up the enviPath instance
    eP = enviPath(INSTANCE_HOST)

    # Who am I?
    print(eP.who_am_i().get_name())

    # Login to access protected packages
    # eP.login('MyUsername', 'SafeIsntIt')
    # print(eP.who_am_i().get_name())

    # objects can be acquired in two different ways:
    # Either managed via the created enviPath instance ...
    # p = eP.get_package(EAWAG_BBD)
    # or by creating a package manually
    bbd_package = Package(eP.requester, id=EAWAG_BBD)

    # Getting data from packages
    compounds = bbd_package.get_compounds()
    print("Number of Compounds in Package {}: {}".format(bbd_package.get_name(), len(compounds)))
    for compound in compounds[:100]:
        print("SMILES of Compound {} -> {}".format(compound.get_name(), compound.get_smiles()))

    rules = bbd_package.get_rules()
    print("Number of Rules in Package {}: {}".format(bbd_package.get_name(), len(rules)))
    for rule in rules[:100]:
        if type(rule) == SimpleRule:
            print("SMIRKS of {} -> {}".format(rule.get_name(), rule.get_smirks()))

    # Create or obtain a package
    # group = eP.who_am_i().get_default_group()
    # my_package = Package.create(eP, group, name='My Package', description='Description of my Package')
    my_package = eP.get_package(ANONYMOUS_PACKAGE)

    # Creating a compound
    # To create data each object provides a static "create" method.
    compound_smiles = 'CC(C)C=CCCCCC(=O)NCC1=CC=C(C(=C1)OC)O'
    compound_name = 'Compound created via lib'
    compound_description = 'A Compound that was created by using this lib'
    # first parameter is the package in which the compound should be stored
    c = Compound.create(my_package, compound_smiles, name=compound_name, description=compound_description)
    print(c)

    # Creating a rule
    # first parameter is the package in which the rule should be stored
    rule_smirks = '[H][#8]-[#7:3]=[#6:4]([H])-[$([#1,*]):6]>>[$([#1,*]):6][C:4]#[N:3]'
    rule_name = 'Rule created via lib'
    rule_description = 'A SimpleRule created by using this lib'
    r = SimpleRule.create(my_package, smirks=rule_smirks, name=rule_name, description=rule_description)
    print(r)

    # Predicting a pathway
    # There are several way to predict a pathway:
    # 1. via the package by calling
    # my_package.predict(...) or my_package.add_pathway(...)
    # 2. Pathway.create(...)
    pw = Pathway.create(my_package, smiles='c1ccccc1', name='My Pathway')

    while not pw.is_completed() and not pw.has_failed():
        sleep(3)

    nodes = pw.get_nodes()
    for node in nodes:
        print(node)

    # eP.logout()