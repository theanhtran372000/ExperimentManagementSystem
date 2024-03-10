import yaml
import pprint
import streamlit as st
from loguru import logger

from utils.request import *
from utils.exp import *


# Load configs
with open('configs.yaml',  'r') as f:
    configs = yaml.full_load(f)
logger.info('Configs: {}'.format(pprint.pformat(configs)))

sender = RequestSender(configs)

# Configure wide screen mode
st.set_page_config(layout="wide")

# Apply CSS
st.markdown('''<style>
    div[data-testid="stMetric"] {
        text-align: center;
    } 
    
    div[data-testid="stMetric"] svg {
        display: none;
    }  
    
    label[data-testid="stMetricLabel"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }          
    
    label[data-testid="stMetricLabel"] p {
        font-size: 18px;
        color: gray;
    }
    
    div[data-testid="stMetricDelta"] > div {
        font-size: 14px;
        font-weight: 600;
        color: #70ae3b;
    }
    
    div[data-testid="stMetricValue"] > div {
        font-size: 28px;
        font-weight: 600;
    }
    
</style>''', unsafe_allow_html=True)

# Main page
st.header('Welcome to Experiment Management System!')
st.caption('By The Anh Tran')

# Fetch data from server
response = sender.experiment_list()

# Display result
if not response['success']:
    st.error('Failed to fetch data from server!', icon='🚨')
    st.info('Error message: {}'.format(response['message']), icon='ℹ️')
else:
    st.success('Fetched data from server successfully!', icon="✅")
    exp_list = response['data']
    
    st.subheader('Here are some statistics.')
    st.markdown('---')
    
    # Display data
    cols = st.columns(4)

    # Display statistics
    classified_exps = experiment_classify(exp_list)
    cols[0].metric(label="Total", value=len(exp_list), delta='Experiments')
    cols[1].metric(label="Created", value=len(classified_exps['created']), delta='Experiments')
    cols[2].metric(label="Running", value=len(classified_exps['running']), delta='Experiments')
    cols[3].metric(label="Done", value=len(classified_exps['done']), delta='Experiments')
    
    cols[0].markdown('---')
    cols[1].markdown('---')
    cols[2].markdown('---')
    cols[3].markdown('---')
    
    exp_sorted_by_accuracy = experiment_sort(
        classified_exps, 
        criterion='accuracy', 
        reverse=True, 
        train=False
    )
    cols[0].metric(
        label="Best Accuracy", 
        value='--' if exp_sorted_by_accuracy is None \
            else "{:.2f}%".format(
                exp_sorted_by_accuracy[0]['result']['train']['accuracy'] * 100
            ), 
        delta='--' if exp_sorted_by_accuracy is None else exp_sorted_by_accuracy[0]['id']
    )
    
    exp_sorted_by_precision = experiment_sort(
        classified_exps, 
        criterion='precision', 
        reverse=True, 
        train=False
    )
    cols[1].metric(
        label="Best Precision", 
        value='--' if exp_sorted_by_precision is None \
            else "{:.2f}%".format(
                exp_sorted_by_precision[0]['result']['train']['precision']['macro'] * 100
            ), 
        delta='--' if exp_sorted_by_precision is None else exp_sorted_by_precision[0]['id']
    )
    
    exp_sorted_by_recall = experiment_sort(
        classified_exps, 
        criterion='recall', 
        reverse=True, 
        train=False
    )
    cols[2].metric(
        label="Best Recall", 
        value='--' if exp_sorted_by_recall is None \
            else "{:.2f}%".format(
                exp_sorted_by_recall[0]['result']['train']['recall']['macro'] * 100
            ), 
        delta='--' if exp_sorted_by_recall is None else exp_sorted_by_recall[0]['id']
    )
    
    exp_sorted_by_duration = experiment_sort(
        classified_exps, 
        criterion='duration', 
        reverse=False
    )
    cols[3].metric(
        label="Fastest", 
        value='--' if exp_sorted_by_duration is None \
            else "{:.2f}s".format(
                exp_sorted_by_duration[0]['run']['dur']
            ), 
        delta='--' if exp_sorted_by_duration is None else exp_sorted_by_duration[0]['id']
    )