class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"Item with ID {item_id} not found"
        super().__init__(self.message)

class ItemAlreadyExistsException(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name
        self.message = f"Item with name '{item_name}' already exists"
        super().__init__(self.message)
