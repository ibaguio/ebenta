#img utils

#returns the image format
def getImageFormat(image):
    if image[1:4] == 'PNG': return 'png'
    if image[0:3] == 'GIF': return 'gif'
    if image[6:10] == 'JFIF': return 'jpeg'
    return None