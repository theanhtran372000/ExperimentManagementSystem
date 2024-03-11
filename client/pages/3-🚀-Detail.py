import os
import time
import streamlit as st

from utils import *


# Load configs
host = os.environ.get('HOST')
sender = RequestSender(host)

# Configure wide screen mode
st.set_page_config(layout="wide")

st.markdown('''
    <style>
        div[data-testid="stTextInput"] input {
            background-color: #dbe6f4;
        }
        
        button[data-testid="baseButton-secondary"] {
            width: 100%;
            background-color: #dbe6f4;
            border: none;
            transition: .3s all;
        }
        
        button[data-testid="baseButton-secondary"]:hover {
            border: 2px solid #004280;
            color: #004280;
        }
    </style>            
''', unsafe_allow_html=True)

# Header
st.header('🚀 Experiment in detail.')
st.info('In this page, we provide experiment information in detail.', icon='ℹ️')

# Body
cols = st.columns([3, 1, 2])
fetch_announce = cols[0].info('Here is some announcements.', icon='ℹ️')

# Select experiment ID
exp_id = cols[2].text_input(
    'Experiment Id', 
    value='' if 'exp_id' not in st.session_state \
        else st.session_state['exp_id'],
    placeholder='🔍 Input Experiment Id here.',
    label_visibility='collapsed'
)

st.session_state['exp_id'] = exp_id

# Fetch data
response = sender.experiment_info(exp_id)

if response['success']:
    fetch_announce.success("Fetch experiment {} data success!".format(exp_id), icon="✅")
    
    st.markdown('---')
    
    data = response['data']
    
    # Display process bar
    st.subheader('🚢 Experiment process')
    
    # Get current status
    curr_status = data['status']['run']['status']
    curr_epoch = data['status']['run']['curr_epoch'] if 'curr_epoch' in data['status']['run'] else None
    total_epoch = data['config']['train']['num_epochs']
    
    curr_progress, curr_text = get_current_progress(curr_epoch, total_epoch, curr_status)
    status_cols = st.columns([5, 1])
    status_cols[0].progress(curr_progress, curr_text)
    if curr_status == 'create':
        start_button = status_cols[1].button('Start this')
        
        if start_button:
            response = sender.experiment_start(exp_id)
            
            if response['success']:
                st.rerun()
    st.markdown('---')
    
    st.subheader('🌍 Experiment info')
    info_cols = st.columns([2, 1])
    
    # Display model info
    info_cols[0].markdown('**Model structure**')
    info_cols[0].info('Here are the visualization of model structure.', icon='ℹ️')
    info_cols[0].code(data['model'].strip())
    info_cols[0].markdown('---')
    
    # Display status
    info_cols[0].markdown('**Training params**')
    info_cols[0].info('Here are the training process information.', icon='ℹ️')
    # info_cols[0].json(data['config'])
    
    smaller_cols = info_cols[0].columns(3)
    smaller_cols[0].markdown('1. Learning rate: **{}**'.format(data['config']['train']['lr']))
    smaller_cols[0].markdown('4. Batch size: **{}**'.format(data['config']['train']['batch_size']))
    
    smaller_cols[1].markdown('2. Num epochs: **{}**'.format(data['config']['train']['num_epochs']))
    smaller_cols[1].markdown('5. Log every: **{}**'.format(data['config']['train']['log_every']))
    
    smaller_cols[2].markdown('3. Loss: **{}**'.format(data['config']['train']['loss']))
    smaller_cols[2].markdown('6. Optim: **{}**'.format(data['config']['train']['optim']))
    
    info_cols[0].markdown('---')
    
    info_cols[0].markdown('**Data augmentation**')
    info_cols[0].info('All data augmentation methods are used in this experiment.', icon='ℹ️')
    
    smaller_cols = info_cols[0].columns(3)
    for i, transform in enumerate(data['config']['data']['transforms']):
        smaller_cols[i % 3].markdown('- Method {}: **{}**'.format(i + 1, transform['name']))
    
    # Display training configs
    
    info_cols[1].markdown('**Timestamp**')
    info_cols[1].info('All timestamps in experiment.', icon='ℹ️')
    
    info_cols[1].markdown('- Create at: **{}**'.format(
        data['status']['run']['create'][:-7] if 'create' in data['status']['run'] else '--'
    ))
    info_cols[1].markdown('- Start at: **{}**'.format(
        data['status']['run']['start'][:-7] if 'start' in data['status']['run'] else '--'
    ))
    info_cols[1].markdown('- End at: **{}**'.format(
        data['status']['run']['end'][:-7] if 'end' in data['status']['run'] else '--'
    ))
    info_cols[1].markdown('- Duration: **{}**'.format(
        '{:.2f}s'.format(data['status']['run']['dur']) if 'dur' in data['status']['run'] else '--'
    ))
    
    info_cols[1].markdown('---')
    info_cols[1].markdown('**Evaluating result**')
    info_cols[1].info('Result of evaluating best checkpoint.', icon='ℹ️')
    
    if 'result' not in data['status']:
        info_cols[1].info('Results are not available.', icon='ℹ️')
    else:
        result_cols = info_cols[1].columns(2)
        
        result_cols[0].success("On train set", icon="✅")
        result_cols[0].markdown('- Accuracy: **{:.2f}%**'.format(data['status']['result']['train']['accuracy'] * 100))
        result_cols[0].markdown('- Precision: **{:.2f}%**'.format(data['status']['result']['train']['precision']['macro'] * 100))
        result_cols[0].markdown('- Recall: **{:.2f}%**'.format(data['status']['result']['train']['recall']['macro'] * 100))
        
        result_cols[1].success("On valid set", icon="✅")
        result_cols[1].markdown('- Accuracy: **{:.2f}%**'.format(data['status']['result']['valid']['accuracy'] * 100))
        result_cols[1].markdown('- Precision: **{:.2f}%**'.format(data['status']['result']['valid']['precision']['macro'] * 100))
        result_cols[1].markdown('- Recall: **{:.2f}%**'.format(data['status']['result']['valid']['recall']['macro'] * 100))
    
else:
    fetch_announce.error('Fetch data failed: {}'.format(response['message']), icon='🚨')
    
    
while True:
    time.sleep(5)
    st.rerun()