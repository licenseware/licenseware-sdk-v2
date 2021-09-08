"""

Here are report components css style properties.
Styles set will determine how the component will look on page.


Usage:

from ...report_components.style_attributes import styles



"""

from dataclasses import dataclass, field

@dataclass
class Styles:
    WIDTH_ONE_THIRD:dict = field(default_factory=lambda:{'width': '1/3'}) 
    WIDTH_FULL:dict = field(default_factory=lambda:{'width': 'full'})
    
        
styles = Styles() # default_factory needs instantiation

