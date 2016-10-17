"""
A first-draft port of the Gemini database to the GA4GH API.

Implement the following functions.  I believe that the function names represent
the GA4GH API, and implementing them requires querying the gemini sqlite
database.
"""


DATABASE_LOCATION = '/home/username/gemini/my.db'


def get_variant(variant_id):
    """Handles requests to the /variants/<variant id> endpoint""" 
    import subprocess, json
    query_string = 'select start,end,variant_id,info,ref,alt from variants where variant_id = %s' % variant_id
    cmd_string = "gemini query -q '%s' %s" % query_string
    cmd_string = cmd_string % DATABASE_LOCATION
    result = subprocess.check_output(cmd_string, shell=True).split()
    data = dict()
    data['start'] = result[0]
    data['end'] = result[1]
    data['id'] = result[2]
    if result[3] and result[3] != 'None':
        d['info'] = result[3]
    data['ref'] = result[4]
    data['alt'] = result[5]
    return json.dumps(d)


def get_variant_set(variant_set_id):
    """It's easy enough, if the GA4GH API provides a standard get-on-ID
    operation, and thankfully Gemini already simply has a table called
    'variants' with which you can 'get' based on ID.

    This method relies on using the vcf_id field of the 'variants'
    table. The theory is that we can compute the correct variant set via
    the distinct values for this field from each row."""
    import subprocess, json
    cmd_string = "gemini query -q 'select distinct vcf_id from variants' %s"
    cmd_string = cmd_string % DATABASE_LOCATION
    result = subprocess.check_output(cmd_string, shell=True).split()
    return json.dumps(len(result))


def search_call_sets(body):
    return 'do some magic!'

def search_variant_sets(body):
    return 'do some magic!'

def search_variants(body):
    return 'do some magic!'

def get_call_set(callSetId):
    return 'do some magic!'
