from copy import deepcopy
from typing import Dict, AnyStr, Union, List, Optional

from dash import Output, Input, html, dash, ALL, ALLSMALLER, MATCH

from . import _callback_transfer


class DuplicateOutputManager:
    """
    -- WARNING --
    На данный момент не поддерживается ALL, ALLSMALLER для component_id с типом dict
    """

    def __init__(self, app: dash.Dash) -> None:

        self.__controller = RelationshipController(app)
        self.__div_data_set_elements: Optional[List[html.Div]] = None

        self._init_app(app)

    def __call__(self, component_id: Union[AnyStr, Dict], component_property: AnyStr) -> Output:

        output = self.__controller.add_relationship_and_get_output_on_dataset(component_id, component_property)

        return output

    def to_plotly_json(self) -> Dict:

        if self.__div_data_set_elements is None:
            self.__div_data_set_elements = self.__controller.register_callbacks_transfer_and_get_divs_data_sets()

        as_json = {
            "props": {'children': self.__div_data_set_elements},
            "type": 'Div',
            "namespace": 'dash_html_components'
        }

        return as_json

    def _init_app(self, app: dash.Dash) -> None:

        app._extra_components.append(self)

        app._inline_scripts.append(_callback_transfer.get_inline_clientside_function_for_register())

        setattr(app, 'DuplicateOutput', self)


class RelationshipController:

    def __init__(self, app: dash.Dash):
        self.app = app
        self.__scheme_relationships = dict()
        self.__component_id_type_dict = dict()

    def add_relationship_and_get_output_on_dataset(self, component_id, component_property) -> dash.Output:

        str_component_id = self._id_dict_to_str(component_id)

        div_data_set_id = _TEMPLATE_DIV_DATA_SET_ID.format(id=str_component_id, property=component_property)
        new_attribute_name = self._make_attribute_name(str_component_id, component_property)

        if str_component_id in self.__component_id_type_dict.keys():
            div_data_set_id = dict(type=div_data_set_id, index=MATCH)

        return Output(div_data_set_id, new_attribute_name)

    def register_callbacks_transfer_and_get_divs_data_sets(self) -> List[html.Div]:

        all_div_data_set_elements = list()

        for component_id in self.__scheme_relationships.keys():
            for component_property in self.__scheme_relationships[component_id].keys():
                div_data_set_elements = self._add_callback(component_id, component_property)
                all_div_data_set_elements.extend(div_data_set_elements)

        return all_div_data_set_elements

    def _id_dict_to_str(self, component_id: Union[Dict, AnyStr]) -> AnyStr:

        if isinstance(component_id, str):
            return component_id

        assert component_id['index'] not in [ALL, ALLSMALLER], (
            'Над данный момент нет поддержки index ALL и ALLSMALLER.'
            'Приносим свои извинения. Актуально на 16.03.2023.'
        )

        copy_component_id = deepcopy(component_id)

        indices = copy_component_id.get('indices')
        str_component_id = copy_component_id['type']

        if not self.__component_id_type_dict.get(str_component_id):
            self.__component_id_type_dict[str_component_id] = indices

        return str_component_id

    def _make_attribute_name(self, component_id: AnyStr, component_property: AnyStr) -> AnyStr:

        if component_id not in self.__scheme_relationships.keys():
            self.__scheme_relationships.update({component_id: dict()})

        if component_property not in self.__scheme_relationships[component_id].keys():
            self.__scheme_relationships[component_id].update({component_property: list()})

        attribute_names = self.__scheme_relationships[component_id][component_property]
        new_attribute_name = _TEMPLATE_DATA_SET_ATTR.format(value=str(len(attribute_names) + 1))

        attribute_names.append(new_attribute_name)

        return new_attribute_name

    def _add_callback(self, component_id: AnyStr, component_property: AnyStr) -> List:

        attribute_names = self.__scheme_relationships[component_id][component_property]
        dict_attribute_names = {attribute_name: '' for attribute_name in attribute_names}
        div_data_set_id = _TEMPLATE_DIV_DATA_SET_ID.format(id=component_id, property=component_property)

        if component_id in self.__component_id_type_dict.keys():
            indices = self.__component_id_type_dict[component_id]
            if not indices:
                raise ValueError(
                    'Используя DuplicateOutput c MATCH необходимо хотя бы в одном '
                    'объекте передать список индексов, которые могут быть. '
                    'Пример: component_id={"type":"table", "index": MATCH, "indices": ["dynamic", "repair"]}'
                )

            component_id = dict(type=component_id, index=MATCH)
            div_data_set_id = dict(type=div_data_set_id, index=MATCH)
            div_data_sets = [
                html.Div(id=dict(type=div_data_set_id['type'], index=index), **dict_attribute_names)
                for index in indices
            ]
        else:
            div_data_sets = [html.Div(id=div_data_set_id, **dict_attribute_names)]

        self.app.clientside_callback(
            _callback_transfer.get_clientside_function(),
            Output(component_id, component_property),
            [Input(div_data_set_id, attr_name) for attr_name in attribute_names],
            prevent_initial_call=True
        )

        return div_data_sets


# utils

_TEMPLATE_DIV_DATA_SET_ID = 'DO-{id}-{property}'
_TEMPLATE_DATA_SET_ATTR = 'data-{value}'