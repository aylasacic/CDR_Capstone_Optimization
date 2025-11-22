# quantum_mitigation/mitigation.py

def mitigate_expectation(unmitigated_val, model):
    '''
        mitigate the input value (unmitigated) using model previously trained 
        parameters:
        - unmitigated_val (float): the unmitigated noisy circuit value
        - model (): sklearn model intercept and coefficient saved previously

        return:
        float: the mitigated value (mitigated_val) given the trained model parameters
    '''
    mitigated_val = model.coef_[0] * unmitigated_val + model.intercept_
    return mitigated_val
