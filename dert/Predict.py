import math

from PIL import Image
import requests
import matplotlib.pyplot as plt

#import ipywidgets as widgets
#from IPython.display import display, clear_output

import torch
from torch import nn
from torchvision.models import resnet50
import torchvision.transforms as T
from hubconf import*
from util.misc import nested_tensor_from_tensor_list
torch.set_grad_enabled(False)

# COCO classes
CLASSES = [
    'background','person'
    # 'background','circle'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098]]

# standard PyTorch mean-std input image normalization
transform = T.Compose([
    T.Resize(800),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def plot_results(pil_img, prob, boxes):
    plt.figure(figsize=(16,10))
    plt.imshow(pil_img)
    ax = plt.gca()
    colors = COLORS * 100
    print(boxes.tolist())
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        cl = p.argmax()
        text = f'{CLASSES[cl]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()


def detect(im, model, transform):
    # mean-std normalize the input image (batch-size: 1)
    img = transform(im).unsqueeze(0)

    # propagate through the model
    outputs = model(img)

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > 0.00001

    # convert boxes from [0; 1] to image scales
    bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], im.size)
    return probas[keep], bboxes_scaled

def predict(im, model, transform):
    # mean-std normalize the input image (batch-size: 1)
    anImg = transform(im)
    data = nested_tensor_from_tensor_list([anImg])

    # propagate through the model
    outputs = model(data)

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    
    keep = probas.max(-1).values > 0.7
    #print(probas[keep])

    # convert boxes from [0; 1] to image scales
    bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], im.size)
    return probas[keep], bboxes_scaled

if __name__ == "__main__":

    model=detr_resnet50(False,2)
    #state_dict = torch.load("outputs/checkpoint.pth",map_location='cpu')
    
    state_dict = torch.load("outputs_new/checkpoint.pth",map_location='cpu')
    model.load_state_dict(state_dict["model"])
    model.eval()

    # im = Image.open('C://Users/18242/Desktop/微流控数据集/000001.jpg')
    im = Image.open('/Users/teresa/Downloads/test02.jpg')

    
    im = im.convert("RGB")
    # im = Image.open('E://zlab-Annotator/annotator/src/annotator-front/public/train/train_2023_1022/ssm01.png')
    scores, boxes = predict(im, model, transform)
    plot_results(im, scores, boxes)






