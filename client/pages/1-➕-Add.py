import yaml
import pprint
import streamlit as st
from loguru import logger

from utils.request import *

# Load configs
with open('configs.yaml',  'r') as f:
    configs = yaml.full_load(f)
logger.info('Configs: {}'.format(pprint.pformat(configs)))

sender = RequestSender(configs)


# Configure wide screen mode
st.set_page_config(layout="wide")

# Main page
st.header('Add new experiment here.')
st.info('In this page, you can customize your own experiment. Customization includes **model structure** and **training parameters**.', icon='ℹ️')
st.markdown('---')

# Add style
st.markdown('''
    <style>
        button[data-testid="baseButton-secondary"] {
            width: 100%;
        }
        
        div[data-testid="column"]:first-child {
            padding-right: 12px;
        }
        
        div[data-testid="column"]:last-child {
            padding-left: 12px;
        }
    </style>
''', unsafe_allow_html=True)

cols = st.columns([3, 2])

### MODEL STRUCTURE ###
cols[0].subheader('Model structure')

if 'layers' not in st.session_state or len(st.session_state['layers']) == 0:
    cols[0].info('Click button below to add a new layer.', icon='ℹ️')
else:
    for i, layer in enumerate(st.session_state['layers']):
        if 'name' not in layer:
            cols[0].markdown('**[{}] Empty layer**'.format(i))
            selected_name = cols[0].selectbox(
                'Select layer name',
                [
                    'none', 'linear', 'flatten', 'dropout',
                    'relu', 'leaky_relu', 'elu',
                    'sigmoid', 'log_sigmoid',
                    'tanh', 'softmax', 'log_softmax'
                ],
                key='{}_empty_layer'.format(i),
                label_visibility='collapsed',
                index=0
            )
            
            if selected_name != 'none':
                st.session_state['layers'][i]['name'] = selected_name
                st.rerun()
        
        else:

            #  Linear layer
            if layer['name'] == 'linear':
                cols[0].markdown('**[{}] Linear layer**'.format(i))
                _cols = cols[0].columns(2)
                
                in_shape = _cols[0].number_input(
                    label='Select input size',
                    min_value=0,
                    max_value=2048,
                    value=784,
                    key='{}_linear_in_shape'.format(i)
                )
                st.session_state['layers'][i]['in_shape'] = in_shape
                
                out_shape = _cols[1].number_input(
                    label='Select output size',
                    min_value=0,
                    max_value=2048,
                    value=784,
                    key='{}_linear_out_shape'.format(i)
                )
                st.session_state['layers'][i]['out_shape'] = out_shape
            
            elif layer['name'] == 'flatten':
                cols[0].markdown('**[{}] Flatten layer**'.format(i))
            
            elif layer['name'] == 'dropout':
                cols[0].markdown('**[{}] Dropout layer**'.format(i))
                
                prob = cols[0].number_input(
                    label='Select dropout probability',
                    min_value=0.0,
                    max_value=1.0,
                    value=0.5,
                    key='{}_dropout_prob'.format(i),
                    step=0.01
                )
                
                st.session_state['layers'][i]['prob'] = prob
                
            elif layer['name'] == 'relu':
                cols[0].markdown('**[{}] ReLU layer**'.format(i))
                
            elif layer['name'] == 'leaky_relu':
                cols[0].markdown('**[{}] Leaky ReLU layer**'.format(i))
                
                slope = cols[0].number_input(
                    label='Select slope',
                    min_value=0.0,
                    max_value=1.0,
                    value=0.01,
                    step=0.001,
                    format='%.3f',
                    key='{}_leaky_relu_slope'.format(i)
                )
                
                st.session_state['layers'][i]['slope'] = slope
                
            elif layer['name'] == 'elu':
                cols[0].markdown('**[{}] ELU layer**'.format(i))
                
                alpha = cols[0].number_input(
                    label='Select alpha',
                    min_value=0.0,
                    max_value=2.0,
                    value=1.0,
                    step=0.01,
                    key='{}_elu_alpha'.format(i)
                )
                
                st.session_state['layers'][i]['alpha'] = alpha
                
            elif layer['name'] == 'sigmoid':
                cols[0].markdown('**[{}] Sigmoid layer**'.format(i))
                
            elif layer['name'] == 'log_sigmoid':
                cols[0].markdown('**[{}] Log Sigmoid layer**'.format(i))
                
            elif layer['name'] == 'tanh':
                cols[0].markdown('**[{}] Tanh layer**'.format(i))
                
            elif layer['name'] == 'softmax':
                cols[0].markdown('**[{}] Softmax layer**'.format(i))
                
            elif layer['name'] == 'log_softmax':
                cols[0].markdown('**[{}] Log Softmax layer**'.format(i))
                
            else:
                logger.error('Layer {} unsupported!'.format(layer['name']))
                pass

_cols = cols[0].columns(2)
add_button = _cols[0].button(label='Add new layer')
if add_button:
    
    if 'layers' not in st.session_state:
        st.session_state['layers'] = []
        st.session_state['layers'].append({})
    else:
        st.session_state['layers'].append({})
    
    # Reset page
    st.rerun()

reset_button = _cols[1].button(label='Reset structure')
if reset_button:
    if 'layers' in st.session_state:
        st.session_state['layers'] = []
        st.rerun()

### TRAINING PARAMS ###
cols[1].subheader('Training Params')
if 'train' not in st.session_state:
    st.session_state['train'] = {}

# Learning rate
lr = cols[1].number_input(
    'Input learning rate', 
    min_value=0.0, max_value=10.0,
    step=0.0001, value=0.01, key='lr',
    format='%.4f'
)
st.session_state['train']['lr'] = lr

# Batch size
batch_size = cols[1].number_input(
    'Input batch size', 
    min_value=1, max_value=1024,
    step=1, value=64, key='batch_size'
)
st.session_state['train']['batch_size'] = batch_size

# Number epochs
num_epochs = cols[1].number_input(
    'Input number of epochs', 
    min_value=1, max_value=100,
    step=1, value=10, key='num_epochs'
)
st.session_state['train']['num_epochs'] = num_epochs

# Loss
loss = cols[1].selectbox(
    'Choose loss',
    [
        'cross_entropy',
        'mse',
        'smooth_l1'
    ],
    key='loss'
)
st.session_state['train']['loss'] = loss

# Optimizer
optim = cols[1].selectbox(
    'Choose optimizer',
    [
        'gradient_descent',
        'adam',
        'rmsprop',
        'adagrad'
    ],
    key='optimizer'
)
st.session_state['train']['optim'] = optim

### DATA AUGMENTATION ###
cols[1].markdown('---')
cols[1].subheader('Data Augmentation')

if 'transforms' not in st.session_state:
    st.session_state['transforms'] = []
    
transforms = cols[1].multiselect(
    'Choose data augmentation methods', 
    ['to_tensor'],
    ['to_tensor'],
    key='transform_list'
)

processed_transforms = []
for transform in transforms:
    processed_transforms.append({
        'name': transform
    })
st.session_state['transforms'] = processed_transforms

st.sidebar.header('Control Panel')

id_display = st.sidebar.markdown('Current id: **none**')
annouce = st.sidebar.info('Here is some announcements.', icon='ℹ️')

button_cols = st.sidebar.columns(2)
create_button = button_cols[0].button('Create', key='create_button')
if create_button:
    
    if 'layers' not in st.session_state or \
        any([
            not bool(layer) for layer in st.session_state['layers']
        ]):
        annouce.error("Your model can't be empty!", icon='🚨')
        
    else:
        
        # Prepare data
        exp_configs = {}
        exp_configs['model'] = {}
        exp_configs['model']['layers'] = st.session_state['layers']
        
        # Prepare training params
        exp_configs['train'] = st.session_state['train']
        
        # Prepare augmentation
        exp_configs['data'] = {}
        exp_configs['data']['transforms'] = st.session_state['transforms']
        
        # Send request
        response = sender.experiment_create(exp_configs)
        if response['success']:
            exp_id = response['data']['id']
            st.session_state['exp_id'] = exp_id
            
            annouce.success("Experiment created with id {}".format(exp_id), icon="✅")
            id_display.markdown("Current id: **{}**".format(exp_id))
        else:
            annouce.error('Create failed: {}'.format(response['message']), icon='🚨')
            
start_button = button_cols[1].button('Start')
if start_button:
    
    if 'exp_id' in st.session_state:
        response = sender.experiment_start(st.session_state['exp_id'])
    
        if response['success']:
            annouce.success("Experiment {} is running...".format(st.session_state['exp_id']), icon="✅")
        else:
            annouce.error('Create failed: {}'.format(response['message']), icon='🚨')
            
    else:
        annouce.error('Unknown experiment id!', icon='🚨')