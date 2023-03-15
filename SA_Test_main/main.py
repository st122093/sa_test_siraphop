from fastapi import FastAPI, File, UploadFile
import pandas as pd
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw
import requests

app = FastAPI()

@app.post('/convert_tsv')
async def convert_tsv(file: UploadFile = File(...)):
    try:
        # Read the TSV file using pandas
        df = pd.read_csv(file.file, sep='\t')
        
        # Convert the dataframe to CSV format
        csv_data = df.to_csv(index=False)

        # Convert the CSV format to array of lines string
        csv_array = csv_data.split('\n')[1:-1]
        for n in range(len(csv_array)):
            csv_array[n] = csv_array[n].replace(',', ', ')
        
        # Return a success message
        return {'Message': 'File converted successfully.',
                'CSV data': csv_array}
    except:
        # Return an error message
        return {'Message': 'Input wrong format.'}

@app.get('/draw_box/{x_topleft}/{y_topleft}/{width}/{height}')
async def draw_box(x_topleft, y_topleft, width, height):
    # Convert str to int
    x_topleft = int(x_topleft)
    y_topleft = int(y_topleft)
    width = int(width)
    height = int(height)

    # Open the existing image
    with Image.open('image.png') as img:
        # To check the bounding box can fit into the image ot not
        img_width, img_height = img.size
        if x_topleft >= img_width or y_topleft >= img_height or x_topleft+width >= img_width or y_topleft+height >= img_height:
            return {'Message': 'The bounding box cannot fit into the image.'}
        else:
            # If fit, draw the box
            img_draw = ImageDraw.Draw(img)
            img_draw.rectangle([(x_topleft, y_topleft), (x_topleft+width, y_topleft+height)], outline ='red')
            img.save('drawn_image.png')
            return FileResponse('drawn_image.png', media_type='image/png')

@app.get("/myname2base64/{name}")
def myname2base64(name):
    # Check the name
    if name in ['Siraphop', 'siraphop', 'Babe', 'babe']:
        # If the name is correct, send the name to another Docker
        response = requests.get(f'http://10.5.0.6:8001/{name}')
        return response.json()['base64']
    else:
        # If not, show the error message
        return {'Message': 'Incorrect name.'}