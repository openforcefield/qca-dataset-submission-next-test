from collections import defaultdict, Counter
from pprint import pformat

import qcportal as ptl


## failures and incompletes

### basic results

def get_results(dataset, spec, client):
    ds = dataset
    kwid = ds.list_keywords().reset_index().set_index('keywords').loc[spec, 'id']

    # we go through molecules as a more reliable way to get to result records
    # than ds.get_records
    mols = ds.get_entries().molecule_id.tolist()
    res = _query_results(mols, client, kwid)

    return res


def get_unfinished_results(dataset, spec, client):
    res = get_results(dataset, spec, client)
    res = [r for r in res if r.status != 'COMPLETE']

    return res


def _query_results(molids, client, keywords_id):
    res = []
    ids = list(molids)
    for i in range(0,len(ids),1000):
        ids_i = ids[i:i+1000]
        res_i = client.query_results(molecule=ids_i,
                                     keywords=keywords_id,
                                     status=None)
        res.extend(res_i)

    return res

### optimizations

def get_optimizations(dataset, spec, client, dropna=False):
    ds = dataset

    while True:
        try:
            ds.status(spec)
        except:
            pass
        else:
            break

    if dropna:
        df = ds.df.dropna()
    else:
        df = ds.df

    ids = list(set(i.id for i in df[spec]))
    
    res = _query_procedures(ids, client)    

    return res


def get_unfinished_optimizations(dataset, spec, client, dropna=False):
    res = get_optimizations(dataset, spec, client, dropna=dropna)
    res = [opt for opt in res if opt.status != 'COMPLETE']

    return res


def _query_procedures(ids, client):
    res = []
    ids = list(ids)
    for i in range(0,len(ids),1000):
        ids_i = ids[i:i+1000]
        res_i = client.query_procedures(ids_i)
        res.extend(res_i)
        
    return res

### torsiondrives

def get_torsiondrives(
        dataset, spec, client, noncomplete=False):

    ds = dataset

    while True:
        try:
            ds.status(spec)
        except:
            pass
        else:
            break

    return ds.df[spec].tolist()


def get_torsiondrive_optimizations(
        dataset, spec, client, noncomplete=False):

    ds = dataset

    while True:
        try:
            ds.status(spec)
        except:
            pass
        else:
            break

    optimizations = defaultdict(set)
    for tdr in ds.df[spec]:
        for val in tdr.optimization_history.values():
            optimizations[tdr.id].update(set(val))

    res_opt = {key: _query_procedures(value, client) for key, value in optimizations.items()}
    if noncomplete:
        res_opt = {key: [opt for opt in value if opt.status != 'COMPLETE']
                   for key, value in res_opt.items()}

    return res_opt


def get_unfinished_torsiondrive_optimizations(
        dataset, spec, client, noncomplete=False):

    res_opt = get_torsiondrive_optimizations(dataset, spec, client, noncomplete=noncomplete)

    ds = dataset
    for tdr in ds.df[spec]:
        if tdr.status == 'COMPLETE':
            res_opt.pop(tdr.id, None)

    return res_opt


def merge(datadict):
    res_s = set()
    res = list()
    for val in datadict.values():
        new_ids = set(i.id for i in val) - res_s
        res.extend([i for i in val if i.id in new_ids])
    return res


## error messages

def count_unique_result_error_messages(
        results, full=False, pretty_print=False, tolerate_missing=False):
    errors = defaultdict(set)

    for res in results:
        if res.status != 'ERROR':
            continue

        try:
            err_content = res.get_error()
        except:
            err_content = None

        if tolerate_missing:
            if err_content is None:
                errors[None].add(res.id)
                continue

        if full:
            errors[err_content.error_message].add(res.id)
        else:
            errors[err_content.error_message.split('\n')[-2]].add(res.id)

    errors = dict(errors)

    content = ""
    if pretty_print:
        for count, key, value in sorted([(len(value), key, value) for key, value in errors.items()], reverse=True):
            content += '-------------------------------------\n'
            content += f"count : {count}\n"
            content += '\n'
            content += f'{key}\n'
            content += '\n'
            content += 'ids : \n'
            content += f'{pformat(value, width=80, compact=True)}\n'
            content += '-------------------------------------\n'
        return content
    else:
        return errors


def get_unique_optimization_error_messages(optimizations, full=False):
    if full:
        return set(opt.get_error().error_message
                   for opt in optimizations if opt.status == 'ERROR')
    else:
        return set(opt.get_error().error_message.split('\n')[-2]
                   for opt in optimizations if opt.status == 'ERROR')


count_unique_optimization_error_messages = count_unique_result_error_messages


## restarts

def restart_results(results, client):
    erred = [res.id for res in results if res.status == 'ERROR']
    client.modify_tasks(operation='restart', base_result=erred)
    print(f"Restarted ERRORed results:\n====\n{erred}\n====\n")


def regenerate_results(res, client):
    for r in res:
        if r.status == 'INCOMPLETE':
            print(f"Regnerated INCOMPLETE result `{r.id}`")
            client.modify_tasks(operation='regenerate', base_result=r.id)


restart_optimizations = restart_results


def regenerate_optimizations(optimizations, client):
    for opt in optimizations:
        if opt.status == 'INCOMPLETE' and (opt.final_molecule is not None):
            print(f"Regnerated INCOMPLETE optimization `{opt.id}`")
            client.modify_tasks(operation='regenerate', base_result=opt.id)


def restart_torsiondrives(torsiondrives, client):
    for tdr in torsiondrives:
        if tdr.status == 'ERROR':
            print(f"Restarted ERRORed torsiondrive `{tdr.id}`")
            client.modify_services('restart', procedure_id=tdr.id)


## modify tasks

def retag_results(results, client, compute_tag):
    incomplete = [res.id for res in results if res.status != 'COMPLETE']
    client.modify_tasks(operation='modify', base_result=incomplete, new_tag=compute_tag)
    print(f"Retagged results with `{compute_tag}':\n====\n{incomplete}\n====\n")


retag_optimizations = retag_results


def reprioritize_results(results, client, priority):
    """Priority can be one of "high", "normal", "low".

    """
    from qcportal.models.task_models import PriorityEnum
    priority_map = {"high": PriorityEnum.HIGH,
                    2: PriorityEnum.HIGH,
                    "normal": PriorityEnum.NORMAL,
                    1: PriorityEnum.NORMAL,
                    "low": PriorityEnum.LOW,
                    0: PriorityEnum.LOW,
                    }

    incomplete = [res.id for res in results if res.status != 'COMPLETE']
    client.modify_tasks(operation='modify', base_result=incomplete, new_priority=priority_map[priority])
    print(f"Reprioritized results as `{priority}':\n====\n{incomplete}\n====\n")


reprioritize_optimizations = reprioritize_results
