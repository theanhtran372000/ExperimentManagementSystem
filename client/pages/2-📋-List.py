import os
import streamlit as st

from utils import *


# Load configs
host = os.environ.get('HOST')
sender = RequestSender(host)

# Configure wide screen mode
st.set_page_config(layout="wide")

st.markdown('''
    <style>
        div[data-baseweb="select"] > div > div {
            background-color: #FFD580;
        }
    </style>
''', unsafe_allow_html=True)

# Main page
st.header('📋 Your experiments are listed here.')
st.info('In this page, you can sort experiments by pre-defined metrics.', icon='ℹ️')

# Fetch data from server
response = sender.experiment_list()

# Display result
if not response['success']:
    st.error('Failed to fetch data from server!', icon='🚨')
    st.info('Error message: {}'.format(response['message']), icon='ℹ️')
else:
    exp_list = response['data']
    classified_exps = experiment_classify(exp_list)
    
    # Sort header
    st.subheader('🔬 Experiment list')
    cols = st.columns(4)
    
    cols[0].markdown('**Sort options**')
    cols[0].caption('Sort options for experiments below.')
    
    criterion = cols[1].selectbox(
        'Sort by', 
        [
            'accuracy',
            'precision',
            'recall',
            'duration'
        ],
        index=0
    )
    
    order = cols[2].selectbox(
        'Sort order', 
        [
            'ascending',
            'descending'
        ],
        index=1
    )
    
    if criterion != 'duration':
        dataset = cols[3].selectbox(
        'On dataset', 
        [
            'train',
            'valid'
        ],
        index=0
    )
    
    st.markdown('---')
    
    sorted_exps = experiment_sort(
        classified_exps,
        criterion=criterion,
        train=dataset if 'dataset' in locals() else True,
        reverse=(order == 'descending')
    )
    all_exps = sorted_exps + classified_exps['running'] + classified_exps['created']
    
    if len(all_exps) > 0:
        for i, exp in enumerate(all_exps):
            
            exp_cols = st.columns([4, 5, 4, 4])
            
            # Column 0
            exp_cols[0].markdown('**Experiment**')
            exp_cols[0].markdown('- Index: **{}**'.format(i))
            exp_cols[0].markdown('- Exp ID: **{}**'.format(exp['id']))
            exp_cols[0].markdown('- Status: **{}**'.format(exp['run']['status']))
            
            # Column 1
            exp_cols[1].markdown('**Timestamp**')
            exp_cols[1].markdown('- Start: **{}**'.format(
                exp['run']['start'][:-7] if 'start' in exp['run'] else '--'
            ))
            exp_cols[1].markdown('- End: **{}**'.format(
                exp['run']['end'][:-7] if 'end' in exp['run'] else '--'
            ))
            exp_cols[1].markdown('- Duration: **{}**'.format(
                '{:.2f}s'.format(exp['run']['dur']) if 'dur' in exp['run'] else '--'
            ))
            
            # Column 2
            exp_cols[2].markdown('**Train set**')
            if 'result' in exp:
                exp_cols[2].markdown('- Train accuracy: **{}**'.format(
                    '{:.4f}'.format(
                        exp['result']['train']['accuracy']) \
                            if 'result' in exp else '--'
                ))
                exp_cols[2].markdown('- Train precision: **{}**'.format(
                    '{:.4f}'.format(
                        exp['result']['train']['accuracy']) \
                            if 'result' in exp else '--'
                ))
                exp_cols[2].markdown('- Train recall: **{}**'.format(
                    '{:.4f}'.format(
                        exp['result']['train']['accuracy']) \
                            if 'result' in exp else '--'
                ))
            else:
                exp_cols[2].markdown('--')
                
            # Column 3
            exp_cols[3].markdown('**Valid set**')
            if 'result' in exp:
                exp_cols[3].markdown('- Valid accuracy: **{}**'.format(
                    '{:.4f}'.format(
                        exp['result']['valid']['accuracy']) \
                            if 'result' in exp else '--'
                ))
                exp_cols[3].markdown('- Valid precision: **{}**'.format(
                    '{:.4f}'.format(
                        exp['result']['valid']['precision']['macro']) \
                            if 'result' in exp else '--'
                ))
                exp_cols[3].markdown('- Valid recall: **{}**'.format(
                    '{:.4f}'.format(
                        exp['result']['valid']['recall']['macro']) \
                            if 'result' in exp else '--'
                ))
            else:
                exp_cols[3].markdown('--')
            
            st.markdown('---')
    else:
        st.info('Experiment list is empty!', icon='ℹ️')
    