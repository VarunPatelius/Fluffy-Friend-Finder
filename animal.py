class Animal:
    def __init__(self, data):
        self.data = data
        self.setAttributes()
    
    def setAttributes(self):
        neededAttributes = [
            "age",
            "attributes",
            "breeds",
            "coat",
            "colors",
            "contact",
            "description",
            "distance",
            "environment",
            "gender",
            "name",
            "size",
            "species",
            "status",
            "url",
            "primary_photo_cropped"
        ]

        for attribute in neededAttributes:
            setattr(self, attribute, self.data[attribute])
    
    def __repr__(self):
        return self.name + ": " + str(getattr(self, "description")) + "\n\n"