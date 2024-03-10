import json
import yaml
import requests

class RequestSender:
    def __init__(self, configs):
        self.configs = configs
    
    
    # Prepare endpoint
    def get_url(self, api):
        return 'http://{}:{}{}'.format(
            self.configs['server']['host'],
            self.configs['server']['port'],
            api
        )
    

    # Create
    def experiment_create(self, exp_configs):
        # Prepare url and header
        url = self.get_url('/exp/create')
        headers = { "Content-Type": "application/json" }
        
        # Prepare data
        json_data = json.dumps(exp_configs)
        
        # Send request
        response = requests.post(
            url=url, 
            data=json_data, 
            headers=headers
        )
        
        data = json.loads(response.text)
        return data
    
    
    # List
    def experiment_list(self):
        # Prepare url and header
        url = self.get_url('/exp/list')
        
        # Send request
        response = requests.get(url=url)
        
        data = json.loads(response.text)
        return data
    
    
    # Start
    def experiment_start(self, exp_id):
        # Prepare url and header
        url = self.get_url('/exp/start')
        headers = { "Content-Type": "application/json" }
        
        # Prepare data
        json_data = json.dumps({
            'id': exp_id
        })
        
        # Send request
        response = requests.post(
            url=url, 
            data=json_data, 
            headers=headers
        )
        
        data = json.loads(response.text)
        return data
    

    # Info
    def experiment_info(self, exp_id):
        # Prepare url and header
        url = self.get_url('/exp/info')
        headers = { "Content-Type": "application/json" }
        
        # Prepare data
        json_data = json.dumps({
            'id': exp_id
        })
        
        # Send request
        response = requests.post(
            url=url, 
            data=json_data, 
            headers=headers
        )
        
        data = json.loads(response.text)
        return data
    
    
    # Delete
    def experiment_delete(self, exp_id):
        # Prepare url and header
        url = self.get_url('/exp/info')
        headers = { "Content-Type": "application/json" }
        
        # Prepare data
        json_data = json.dumps({
            'id': exp_id
        })
        
        # Send request
        response = requests.delete(
            url=url, 
            data=json_data, 
            headers=headers
        )
        
        data = json.loads(response.text)
        return data
    
        
if __name__ == '__main__':
    
    with open('../configs.yaml', 'r') as f:
        configs = yaml.full_load(f)
    
    sender = RequestSender(configs)
    data = sender.experiment_list()
    print(data)
    
        
        
        