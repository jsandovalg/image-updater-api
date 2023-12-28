import base64
import json
from io import BytesIO
from PIL import Image, PngImagePlugin
from fastapi import FastAPI, HTTPException
import random
from pydantic import BaseModel
from typing import Dict

app = FastAPI();

@app.get('/')
async def root():
	return {'example': 'This is an example', 'data': 0}

@app.get('/random/{limit}')
async def get_random(limit: int):
	rn: int = random.randint(0, limit)
	return { 'number': rn, 'limit': limit}

class ImageData(BaseModel):
    image_b64: str
    user_comment: Dict  

@app.post('/update_metadata')
async def update_metadata(data: ImageData):
    try:
        new_image_b64 = update_png_metadata(data.image_b64, data.user_comment)
        return {"updated_image": new_image_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Function
def update_png_metadata(image_b64, user_comment):
    # Decode the base64 image
    image_data = base64.b64decode(image_b64)
    image = Image.open(BytesIO(image_data))

    # Ensure the image is in PNG format
    if image.format != 'PNG':
        raise ValueError("The provided image is not a PNG")

	# Convert dictionary to JSON string
    user_comment_str = json.dumps(user_comment)

    # Create a new metadata dictionary
    meta = PngImagePlugin.PngInfo()

    # Adding or updating the custom metadata. This uses the 'tEXt' chunk for textual data.
    meta.add_text("UserComment", user_comment_str)

    # Save the modified image to a bytes buffer with the updated metadata
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG", pnginfo=meta)
    output_buffer.seek(0)  # Move to the beginning of the buffer

    # Return the modified image as base64
    return base64.b64encode(output_buffer.getvalue()).decode('utf-8')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)