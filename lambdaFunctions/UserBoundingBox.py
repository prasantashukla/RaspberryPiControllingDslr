class UserBoundingBox:
    def __init__(self, boundingBox, username, smileConfidence):
        self.boundingBox = boundingBox
        self.username = username
        self.smileConfidence = smileConfidence
    
u = UserBoundingBox("sdfdf", None, 99)
print(u.boundingBox)