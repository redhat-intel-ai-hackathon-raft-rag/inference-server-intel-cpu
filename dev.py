def device_widget():
    import ipywidgets as widgets
    device = widgets.Dropdown(
        options=['cpu', 'cuda'],
        value='cpu',
        description='Device:',
        disabled=False,
    )
    return device


device = device_widget().value
