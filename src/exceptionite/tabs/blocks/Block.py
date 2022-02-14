class Block:
    id = "blockid"
    name = "Block Name"
    icon = "Icon Name"
    component = "KeyValBlock"
    disable_scrubbing = False
    empty_msg = "No content."

    def __init__(self, tab, handler, options={}):
        # tab which holds the block
        self.tab = tab
        self.handler = handler
        self.options = options
        self.data = {}
        assert self.id, "Tab should declare an 'id' attribute !"

    def serialize(self):
        raw_data = self.build()
        self.data = self.handler.scrub_data(raw_data, self.disable_scrubbing)
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "component": self.component,
            "data": self.data,
            "empty_msg": self.empty_msg,
            "has_content": self.has_content(),
        }

    def build(self):
        raise NotImplementedError("block should implement build()")

    def has_content(self):
        return False
