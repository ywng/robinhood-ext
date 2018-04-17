import torch, torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from PIL import Image, ImageOps
import torchvision.transforms as transforms

import numpy as np
import pickle

#transform PIL image to tensor
def image_to_tensor(pil_image):
	normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
	loader = transforms.Compose([transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize])
	return loader(pil_image).unsqueeze(0) #need to add one dimension, need to be 4D to pass into the network

#load model
def load_model():
	num_classes = 120
	model = torchvision.models.densenet121(pretrained=True)
	for param in model.parameters():
	    param.requires_grad = False
	    
	num_features = model.classifier.in_features
	#replace the classifier of the trained network with our dog classifier
	model.classifier = nn.Linear(num_features, num_classes) 

	model.load_state_dict(torch.load('dog-breed-ident-densenet121.pt'))
	model.eval()
	
	return model

#inference
def classify(img):
	model = load_model()
	labels = pickle.load(open("dog_breeds_labels.pickle", "rb"))
	image_tensor = image_to_tensor(img)
	input_var = torch.autograd.Variable(image_tensor, volatile=True)
	output = model(input_var)
	prob = F.softmax(output).cpu().data.numpy()
	class_index = np.argmax(prob)

	return labels[class_index] + " (" + '{0:.1f}'.format(np.max(prob)*100) +"%)"


