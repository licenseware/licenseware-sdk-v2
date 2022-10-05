class Error(Exception):
    pass


class ErrorAlreadyAttached(Error):
    pass


class StyleAttrs:
    """
    Usage:
    ```py

    styles = (
        StyleAttrs()
        .width_one_third
        .set("height", "full")
    )

    ```
    """

    def __init__(self):
        self.metadata = {}

    def set(self, name: str, value: str):
        if name in self.metadata.keys():
            raise ErrorAlreadyAttached(f"Style '{name}' already set")
        self.metadata.update({name: value})
        return self

    @property
    def width_one_third(self):
        if "width" in self.metadata.keys():
            raise ErrorAlreadyAttached("Style 'width' already set")
        self.metadata.update({"width": "1/3"})
        return self

    @property
    def width_two_thirds(self):
        if "width" in self.metadata.keys():  # pragma no cover
            raise ErrorAlreadyAttached("Style 'width' already set")
        self.metadata.update({"width": "2/3"})
        return self

    @property
    def width_full(self):
        if "width" in self.metadata.keys():
            raise ErrorAlreadyAttached("Style 'width' already set")
        self.metadata.update({"width": "full"})
        return self

    @property
    def width_half(self):
        if "width" in self.metadata.keys():
            raise ErrorAlreadyAttached("Style 'width' already set")
        self.metadata.update({"width": "1/2"})
        return self
