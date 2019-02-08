# Algorithm that calculates bounding box overlap area b/w two bounding boxes
# BoundingBox
'''
class BoundingBox
    Left,
    Top,
    Width,
    Height
'''
def getArea(boundingBox):
    return boundingBox.Height * boundingBox.Width

def getOverlapArea(boundingBox1, boundingBox2):
    # boundingBox1 Variables
    l1 = boundingBox1.Left
    t1 = boundingBox1.Top
    w1 = boundingBox1.Width
    h1 = boundingBox1.Height

    # boundingBox2 Variables
    l2 = boundingBox2.Left
    t2 = boundingBox2.Top
    w2 = boundingBox2.Width
    h2 = boundingBox2.Height

    # Check if the boxes are overlapping or not
    # Horizontal Overlapping Check
    horizontal_overlapping = False
    vertical_overlapping = False

    if( ( (l1 <= l2) and ((l1 + w1) >= l2) )  or ( (l2 <= l1) and ((l2 + w2) >= l1) ) ):
        horizontal_overlapping = True

    # Vertical Overlapping Check
    if( (t1 <= t2 and t1 + h1 >= t2) or (t2 <= t1 and t2 + h2 >= t1) ):
        vertical_overlapping = True

    area_of_intersection = 0
    if (horizontal_overlapping and vertical_overlapping):     
        length = abs ((l1 + w1) - (l2))
        
        width = abs((t1 + h1) - (t2))
        
        area_of_intersection = length * width

    area_of_union = getArea(boundingBox1) + getArea(boundingBox2) - area_of_intersection

    overlapAreaPercentage = 100 * area_of_intersection / area_of_union
    print ("overlapArea% = ", overlapAreaPercentage)
    return overlapAreaPercentage