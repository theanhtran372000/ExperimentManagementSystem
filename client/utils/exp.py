

# Classify experiments by their status
def experiment_classify(exps):
    
    classified_exps = {
        'created': [],
        'running': [],
        'done': []
    }
    
    for exp in exps.values():
        if exp['run']['status'] == 'create':
            classified_exps['created'].append(exp)
        elif exp['run']['status'] in ['train', 'eval']:
             classified_exps['running'].append(exp)
        elif exp['run']['status'] == 'done':
            classified_exps['done'].append(exp)
        else:
            pass
        
    return classified_exps


# Sort their experiment by their metrics: accuracy/precision/recall/duration
def experiment_sort(classified_exps, criterion='accuracy', train=True, reverse=True):
    
    # Get done experiments only
    done_exps = classified_exps['done']
    
    if len(done_exps) == 0:
        return None
    
    if criterion == 'duration':
            return sorted(done_exps, key=lambda item: item['run']['dur'], reverse=reverse)
    
    if train:
        if criterion == 'accuracy':
            return sorted(done_exps, key=lambda item: item['result']['train']['accuracy'], reverse=reverse)
        elif criterion == 'precision':
            return sorted(done_exps, key=lambda item: item['result']['train']['precision']['macro'], reverse=reverse)
        elif criterion == 'recall':
            return sorted(done_exps, key=lambda item: item['result']['train']['recall']['macro'], reverse=reverse)
        else:
            return None
    else:
        if criterion == 'accuracy':
            return sorted(done_exps, key=lambda item: item['result']['valid']['accuracy'], reverse=reverse)
        elif criterion == 'precision':
            return sorted(done_exps, key=lambda item: item['result']['valid']['precision']['macro'], reverse=reverse)
        elif criterion == 'recall':
            return sorted(done_exps, key=lambda item: item['result']['valid']['recall']['macro'], reverse=reverse)
        else:
            return None