"""
Usage

from ...report_components import style_props

style_props_list = [style_props.WIDTH_FULL, style_props.HEIGHT_FULL]
style_props_dict = {k: v for dict_ in style_props_list for k, v in dict_.items()}

style_props_list = [{'width': 'full'}, {'height': '100vh'}]
style_props_dict = {'width': 'full', 'height': '100vh'}

"""

from dataclasses import dataclass, field

@dataclass
class Styles:
    WIDTH_ONE_THIRD:dict = field(default_factory=lambda:{'width': '1/3'}) 
    WIDTH_FULL:dict = field(default_factory=lambda:{'width': 'full'})
    
        
style_props = Styles()

