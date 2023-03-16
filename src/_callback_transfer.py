from dash.dependencies import ClientsideFunction


def get_clientside_function() -> ClientsideFunction:

    return ClientsideFunction(
        namespace=_NAMESPACE,
        function_name=_FUNCTION_NAME
    )


def get_inline_clientside_function_for_register() -> str:

    inline_clientside_function = _INLINE_CLIENTSIDE_TEMPLATE.format(
        namespace=_NAMESPACE,
        function_name=_FUNCTION_NAME,
        clientside_function=_TRANSFER_VALUE_FROM_DATA_SET_TO_ORIGINAL_PROPERTY
    )

    return inline_clientside_function


# utils

_NAMESPACE = 'duplicate_output'
_FUNCTION_NAME = 'transfer_value_from_data_set_to_original_property'

_TRANSFER_VALUE_FROM_DATA_SET_TO_ORIGINAL_PROPERTY = """
        function() {
            var triggered = dash_clientside.callback_context.triggered[0];
            var triggered_id_split = triggered['prop_id'].split('.');

            // находим div тег с attribute_name, который вызвал колбек.
            var div_id = document.getElementById(triggered_id_split[0]);
            var attribute_name = triggered_id_split[1].replace('data-', '');

            // проверяем, есть ли атрибут, который вызвал колбек, в наших дата-сет атрибутах.
            if (!Object.keys(div_id.dataset).includes(attribute_name)) {
                return dash_clientside.no_update;
            }

            // чистим data-set, который временно хранил данные.
            div_id.dataset[attribute_name] = '';

            return triggered['value'];
        }
"""

_INLINE_CLIENTSIDE_TEMPLATE = """
    var clientside = window.dash_clientside = window.dash_clientside || {{}};
    var ns = clientside["{namespace}"] = clientside["{namespace}"] || {{}};
    ns["{function_name}"] = {clientside_function};
"""