class InventoryItemImages:

    def __init__(self, api_session, inventory_item, images=[]):
        self.api_session = api_session
        self.inventory_item = inventory_item
        self.images = images
        self.update()

    def __getitem__(self, key):
        if key in self.image_id_lookup:
            return self.images[self.image_id_lookup[key]]
        else:
            return self.images[key]

    def __len__(self):
        return len(self.images)

    def clear(self):
        self.primary = None
        self.image_ids = []
        self.image_id_lookup = {}

    def update(self):
        self.clear()
        for image in self.images:
            self.image_ids.append(image.image_id)
            self.image_id_lookup[image.image_id] = self.images.index(image)
            if image.primary:
                self.primary = image

    def append(self, image):
        self.images.append(image)
        self.update()

    def extend(self, images):
        for image in images:
            self.append(image)
        self.update()

    def add(self, filepath):
        self.inventory_item.add_image(filepath)
