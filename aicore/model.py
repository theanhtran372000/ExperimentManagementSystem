import yaml
from loguru import logger

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms


# Define the model based on configuration
class ConfiguredModel(nn.Module):
    
    def __init__(self, model_configs):
        super().__init__()
        
        self.model_configs = model_configs
        all_layers = []
        
        #  Build network from config
        all_layers = self.build_network()
        
        # Transform into a sequential model
        self.model = nn.Sequential(*all_layers)
        logger.info('Model architecture: \n{}'.format(str(self.model)))


    def build_network(self):
        layer_list = []
        for i, layer in enumerate(self.model_configs['layers']):
            
            # Linear layer
            if layer['name'] == 'linear':
                layer_list.append(
                    nn.Linear(
                        layer['in_shape'], 
                        layer['out_shape']
                    )
                )
                
            # Flatten layer
            elif layer['name'] == 'flatten':
                layer_list.append(nn.Flatten())
            
            # Dropout layer
            elif layer['name'] == 'dropout':
                layer_list.append(
                    nn.Dropout(
                        p=layer['prob'] \
                            if 'prob' in layer else 0.5
                    )
                )
            
            # Activation layer
            elif layer['name'] == 'relu':
                layer_list.append(nn.ReLU())
                
            elif layer['name'] == 'leaky_relu':
                layer_list.append(
                    nn.LeakyReLU(
                        negative_slope=layer['slope'] \
                            if 'slope' in layer else 0.01
                    )
                )
                
            elif layer['name'] == 'elu':
                layer_list.append(
                    nn.ELU(
                        alpha=layer['alpha'] \
                            if 'alpha' in layer else 1.0
                    )
                )
            
            elif layer['name'] == 'sigmoid':
                layer_list.append(nn.Sigmoid())
                
            elif layer['name'] == 'log_sigmoid':
                layer_list.append(nn.LogSigmoid())
                
            elif layer['name'] == 'tanh':
                layer_list.append(nn.Tanh())
            
            elif layer['name'] == 'softmax':
                layer_list.append(nn.Softmax(dim=-1))
                
            elif layer['name'] == 'log_softmax':
                layer_list.append(nn.LogSoftmax(dim=-1))  
            
            else:
                logger.error("Layer type {} unsupported.".format(layer['name']))
                # raise Exception("Layer type {} unsupported.".format(layer['name']))
                pass
            
        return layer_list
    
    def forward(self, x):
        return self.model(x)
    
    # Validate whether the model structure is valid or not
    def is_valid(self):
        
        batch_size  = 32
        image_shape = (1, 28, 28) # (channel, height, width)
        n_classes   = 10
        
        # Create fake batch of image
        test_batch = torch.rand(batch_size, *image_shape)
        
        # Try forward
        try:
            with torch.no_grad():
                output = self.forward(test_batch)
                if output.shape == torch.Size([batch_size, n_classes]):
                    logger.success('Valid model structure.')
                    return True
                else:
                    logger.error('Invalid model structure. Invalid output shape {}.'.format(output.shape))
                    return False
                
        except:
            logger.error('Invalid model structure. Forward exception.')
            return False
        

if __name__ == '__main__':
    
    # Load configs
    config_path = '../configs/experiments/configs.default.yaml'
    with open(config_path, 'r') as f:
        configs = yaml.full_load(f)
        
    # Try build model
    model = ConfiguredModel(configs['model'])
    logger.info('Model: \n{}'.format(str(model)))
    
    # Validate model
    is_valid = model.is_valid()
    if is_valid:
    
        # Set up the training parameters
        batch_size = 64
        learning_rate = 0.01
        num_epochs = 5

        # Load the MNIST dataset
        data_dir = '../data'
        train_dataset = datasets.MNIST(root=data_dir, train=True, transform=transforms.ToTensor(), download=True)
        test_dataset = datasets.MNIST(root=data_dir, train=False, transform=transforms.ToTensor())

        train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

        # Define the loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=learning_rate)

        # Train the model
        total_step = len(train_loader)
        for epoch in range(num_epochs):
            for i, (images, labels) in enumerate(train_loader):
                
                # Forward pass
                outputs = model(images)
                loss = criterion(outputs, labels)

                # Backward and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                if (i+1) % 100 == 0:
                    logger.info('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, total_step, loss.item()))

        # Test the model
        model.eval()
        with torch.no_grad():
            correct = 0
            total = 0
            for images, labels in test_loader:
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            logger.info('Accuracy on the test set: {:.2f}%'.format(100 * correct / total))