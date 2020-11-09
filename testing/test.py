from io import StringIO 
import base64
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import os



from PIL import Image
from io import BytesIO
import base64


file = open('image.txt','r')
imstring = file.read()
file.close()




def ProcessImage(imgstring):
    '''
        IN> Image string in base64
        OUT> FileStorage object 
    '''    

    # tempimg = StringIO.StringIO(imgstring.decode('base64'))
    
    data = ''.join(str(x) for x in imgstring.split(',')[1:])
    file_data = base64.b64decode(data)

    ending = imgstring.split(';')[0].split('/')[1]
    filename = secure_filename('image'+'.'+ending)


    return FileStorage(stream=file_data, filename=filename,content_type='image/'+ending)

    # filename = 'some_ima22ge.jpeg'  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(file_data)
    #     print('saved')
    


f = ProcessImage(imstring)

def testing(x):
    print(x.stream)


testing(f)