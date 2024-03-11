def get_current_progress(
    curr_epoch, 
    total_epoch, 
    status
):
    if status == 'create':
        progress = 0.0
        text = '[0%] Not started!'
        
        return progress, text
    
    elif status == 'train':
        progress = curr_epoch / total_epoch * 0.8
        text = '[{:.0f}%] [{}/{}] Training...'.format(progress * 100, curr_epoch, total_epoch)
        
        return progress, text
    
    elif status == 'eval':
        return 0.8, '[80%] Evaluating...'
    
    elif status == 'done':
        return 1.0, '[100%] Done!'
    
    else:
        return None, None
    