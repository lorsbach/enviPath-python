Install using ``pip``…

::

    pip install -e git+https://github.com/lorsbach/enviPath-python#egg=enviPath-python
    
Quickstart…
::

    from pprint import pprint
    from enviPath_python.enviPath import *
    from enviPath_python.objects import *

    # Define the instance to use                                                                                                                                                                                       
    INSTANCE_HOST = 'https://envipath.org/'
    ep = enviPath(INSTANCE_HOST)

    # Get objects directly via API ..                                                                                                                                                                                  
    p = ep.get_packages()[0]
    pprint(p.get_json())

    # Or create them manually                                                                                                                                                                                    
    ep_r = ep.requester
    data = {
    # EAWAG SOIL identifier                                                                                                                                                                                        
      'id': 'https://envipath.org/package/5882df9c-dae1-4d80-a40e-db4724271456',
    }
    p = Package(ep_r, **data)
    pprint(p)

    # More objects as well as update methods will be implemented…
    c = p.get_compounds()[0]
    pprint(c.get_json())
    pprint(c.get_structures())
