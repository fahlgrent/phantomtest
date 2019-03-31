"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'csv_from_artifacts_1' block
    csv_from_artifacts_1(container=container)

    return

def csv_to_list_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('csv_to_list_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    id_value = container.get('id', None)

    # collect data for 'csv_to_list_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.vaultId', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'csv_to_list_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'list_name': "",
                'vault_id': container_item[0],
                'container_id': id_value,
                'list_id': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("csv to list", parameters=parameters, assets=['csvhome'], name="csv_to_list_1", parent_action=action)

    return

def csv_from_artifacts_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('csv_from_artifacts_1() called')

    id_value = container.get('id', None)

    # collect data for 'csv_from_artifacts_1' call

    parameters = []
    
    # build parameters list for 'csv_from_artifacts_1' call
    parameters.append({
        'container_id': id_value,
        'page_size': 1000,
    })

    phantom.act("csv from artifacts", parameters=parameters, assets=['csvhome'], callback=csv_to_list_1, name="csv_from_artifacts_1")

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return