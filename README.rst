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

    # Create package object
    p = Package(ep.requester, id='https://envipath.org/package/650babc9-9d68-4b73-9332-11972ca26f7b')

    # More objects as well as update methods will be implemented…
    c = p.get_compounds()[0]
    pprint(c.get_json())
    pprint(c.get_structures())

    # Predict...
    pw = p.predict('c1ccccc1', name='Pathway via REST', description='A pathway created via REST')
    pprint(pw.get_json())
    