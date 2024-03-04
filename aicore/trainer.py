import torch.nn as nn
import torch.utils.data as data
import torch.optim as optim
from torchvision import datasets, transforms


class Trainer:
    def __init__(self, model, data_configs, train_configs):
       
       self.model = model
       self.data_configs = data_configs
       self.train_configs = train_configs
       
       # Build transforms
       self.transforms = self.prepare_transforms()
       
       # Prepare dataset
       self.train_dataset = self.prepare_dataset(train=True)
       self.valid_dataset = self.prepare_dataset(train=False)
       
       # Prepare dataloader
       self.train_loader = self.prepare_dataloader(self.train_dataset, shuffle=True)
       self.valid_loader = self.prepare_dataloader(self.valid_dataset, shuffle=False)
       
       # Prepare loss
       self.loss = self.prepare_loss()
       
       # Prepare optimizer
       self.optim = self.prepare_optim()
    
    
    def train(self):
        # TODO: Train model
        pass
    
        
    def eval(self):
        # TODO: Eval model
        pass
    
    
    def save(self):
        # TODO: Save model
        pass
       
    # Prepare transform stack
    def prepare_transforms(self):
        transform_list = []
        
        for transform in self.data_configs['transforms']:
            if transform['name'] == 'to_tensor':
                transform_list.append(transforms.ToTensor())
            else:
                # TODO: Other transforms
                pass
                
        return transforms.Compose(transform_list)
    
    
    # Prepare dataset (download if necessary)
    def prepare_dataset(self, train=True, download=True):
        # Load the MNIST dataset
        return datasets.MNIST(
            root=self.data_configs['dir'], 
            train=train, 
            transform=self.transforms, 
            download=download
        )
    
    
    # Prepare dataloader  
    def prepare_dataloader(self, dataset, shuffle=True):
        return data.DataLoader(
            dataset=dataset, 
            batch_size=self.train_configs['batch_size'], 
            shuffle=shuffle
        )
        
        
    # Prepare loss
    def prepare_loss(self):
        if self.train_configs['loss'] == 'CE':
            return nn.CrossEntropyLoss()
        else:
            # TODO: Other loss
            return None
    
    
    # Prepare optimizer
    def prepare_optim(self):
        if self.train_configs['optim'] == 'GD':
            return optim.SGD(self.model.parameters(), lr=self.train_configs['lr'])
        else:
            # TODO: Other optimizer
            return None