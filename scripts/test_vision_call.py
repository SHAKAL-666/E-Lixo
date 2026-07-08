from google.cloud import vision
from google.cloud.vision import Image
import traceback

try:
    client = vision.ImageAnnotatorClient()
    with open('test_upload.jpg','rb') as f:
        content = f.read()
    image = Image(content=content)
    resp = client.label_detection(image=image)
    if resp.error and resp.error.message:
        print('API_ERROR:', resp.error.message)
    else:
        labels = [l.description for l in resp.label_annotations[:5]]
        print('OK:', labels)
except Exception as e:
    print('EXCEPTION:', type(e).__name__, str(e))
    traceback.print_exc()
