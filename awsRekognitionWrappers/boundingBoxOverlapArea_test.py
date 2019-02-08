import unittest
import boundingBoxOverlapArea as b

class BoundingBox:
    def __init__(self, Left, Top, Width, Height):
        self.Width = Width
        self.Height = Height
        self.Left = Left
        self.Top = Top

b1 = BoundingBox( 0.36954253911972046, 0.3948459327220917, 0.031576842069625854, 0.07638522982597351 )
b2 = BoundingBox( 0.36954253911972046, 0.3948459327220917, 0.031576842069625854, 0.07638522982597351)
overlapAreaPercentage = b.getOverlapArea(b1, b2)
print(overlapAreaPercentage)