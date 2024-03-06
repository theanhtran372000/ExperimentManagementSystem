from loguru import logger
from sklearn.metrics import precision_score, recall_score

import torch
import torch.nn as nn
import torch.utils.data as data
import torch.optim as optim
import torch.nn.functional as F
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
       
       # Running params
       self.min_loss = None
    
    
    # Training function
    def train(self):
        
        self.min_loss = 999
        total_step = len(self.train_loader)
        
        for epoch in range(self.train_configs['num_epochs']):
            
            total_loss = 0.0
            for i, (images, labels) in enumerate(self.train_loader):
                
                # Forward pass
                outputs = self.model(images)
                labels_onehot = F.one_hot(labels, num_classes=10).float()
                
                loss = self.loss(outputs, labels_onehot)
                total_loss += loss * images.shape[0]
                
                # Save checkpoint, update min loss
                if (i+1) % self.train_configs['log_every'] == 0:
                    
                    logger.info('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(
                        epoch + 1, self.train_configs['num_epochs'], 
                        i+1, total_step, loss.item()
                    ))
                    
                # Backward and optimize
                self.optim.zero_grad()
                loss.backward()
                self.optim.step()
            
            # Save checkpoints 
            avg_loss = total_loss / len(self.train_loader.dataset)
            if avg_loss < self.min_loss:
                logger.info('Epoch [{}/{}], Loss update: {:.4f} -> {:.4f}'.format(
                    epoch + 1, self.train_configs['num_epochs'], 
                    self.min_loss, avg_loss
                ))
                self.min_loss = avg_loss
                self.save_checkpoint()       
    
    
    # Evaluating function                 
    def eval(self, train=False):
        
        # Load best checkpoint
        self.load_checkpoint()
        self.model.eval()
        
        # Start evaluation
        with torch.no_grad():
            correct = 0
            total = 0
            true_labels = []
            predicted_labels = []

            for images, labels in self.train_loader if train else self.valid_loader:
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
                true_labels.extend(labels.tolist())
                predicted_labels.extend(predicted.tolist())

            accuracy = correct / total
            precision = precision_score(true_labels, predicted_labels, average='macro', zero_division=0.0)
            recall = recall_score(true_labels, predicted_labels, average='macro', zero_division=0.0)

            logger.info('=== RESULT ON {} SET ==='.format('TRAIN' if train else 'VALID'))
            logger.info('Accuracy: {:.2f}%'.format(accuracy * 100))
            logger.info('Precision: {:.2f}%'.format(precision * 100))
            logger.info('Recall: {:.2f}%'.format(recall * 100))
    
    
    # Save and load checkpoint function
    def save_checkpoint(self):
        torch.save(self.model.state_dict(), 'best_ckpt.pth')
    
    def load_checkpoint(self):
        self.model.load_state_dict(torch.load('best_ckpt.pth'))
    
    
    # Prepare transform stack
    def prepare_transforms(self):
        transform_list = []
        
        for transform in self.data_configs['transforms']:
            if transform['name'] == 'to_tensor':
                transform_list.append(transforms.ToTensor())
            else:
                logger.error('Transform "{}" is under development.'.format(transform['name']))
                # raise Exception('Transform "{}" is under development.'.format(transform['name']))
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
        
        if self.train_configs['loss'] == 'cross_entropy':
            return nn.CrossEntropyLoss()
        
        elif self.train_configs['loss'] == 'mse':
            return nn.MSELoss()
        
        elif self.train_configs['loss'] == 'smooth_l1':
            return nn.SmoothL1Loss()
        
        else:
            logger.error('Loss "{}" is under development.'.format(self.train_configs['loss']))
            # raise Exception('Loss "{}" is under development.'.format(self.train_configs['loss']))
            return None
    
    
    # Prepare optimizer
    def prepare_optim(self):
        
        if self.train_configs['optim'] == 'gradient_descent':
            return optim.SGD(
                self.model.parameters(), 
                lr=self.train_configs['lr']
            )
            
        elif self.train_configs['optim'] == 'adam':
            return optim.Adam(
                self.model.parameters(), 
                lr=self.train_configs['lr']
            )
            
        elif self.train_configs['optim'] == 'rmsprop':
            return optim.RMSprop(
                self.model.parameters(), 
                lr=self.train_configs['lr']
            )
            
        elif self.train_configs['optim'] == 'adagrad':
            return optim.Adagrad(
                self.model.parameters(), 
                lr=self.train_configs['lr']
            )
                
        else:
            logger.error('Optimizer "{}" is under development.'.format(self.train_configs['optim']))
            # raise Exception('Optimizer "{}" is under development.'.format(self.train_configs['optim']))
            return None