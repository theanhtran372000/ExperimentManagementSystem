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
            if layer['name'] == 'linear':
                
                # Flatten if the first layer is linear layer
                if i == 0:
                    layer_list.append(nn.Flatten())
                
                # Add new hidden layer
                layer_list.append(
                    nn.Linear(
                        layer['in_shape'], 
                        layer['out_shape']
                    )
                )
                
                # Add activation function
                if layer['act_func'] == 'relu':
                    layer_list.append(nn.ReLU())
                elif layer['act_func'] == 'softmax':
                    layer_list.append(nn.LogSoftmax(dim=1))    
                else:
                    # TODO: Other activations
                    pass
                
            else:
                # TODO: Other layers
                pass
            
        return layer_list
    
    
    def forward(self, x):
        return self.model(x)

if __name__ == '__main__':
    
    # Load configs
    config_path = '../configs/experiments/linear_configs.default.yaml'
    with open(config_path, 'r') as f:
        configs = yaml.full_load(f)
        
    # Try build model
    model = ConfiguredModel(configs['model'])
    logger.info('Model: \n{}'.format(str(model)))
    
    # Set up the training parameters
    batch_size = 64
    learning_rate = 0.01
    num_epochs = 10

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
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, total_step, loss.item()))

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

        print('Accuracy on the test set: {:.2f}%'.format(100 * correct / total))