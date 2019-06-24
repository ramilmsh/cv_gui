class OrderedHashSet(dict):
    
    def __init__(self):
        super().__init__()
        self.current_id = 0
    
    def append(self, item: object) -> int:
        self[self.current_id] = item
        self.current_id += 1
        return self.current_id - 1
