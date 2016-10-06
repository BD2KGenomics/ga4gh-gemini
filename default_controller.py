"""
A first-draft port of the Gemini database to the GA4GH API.

Some of the API calls may be difficult or impossible to implement, due to the
Gemini schema.
"""


DATABASE_LOCATION = '/home/username/gemini/my.db'


def get_variant(variant_id):
    """Handles requests to the /variants/<variant id> endpoint""" 
    import subprocess, json
    c = "gemini query -q 'select start,end,variant_id,info,ref,alt from variants where variant_id = %s' %s" % (variant_id, DATABASE_LOCATION)
    r = subprocess.check_output(c, shell=True).split()
    d = dict()
    d['start'] = r[0]
    d['end'] = r[1]
    d['id'] = r[2]
    if r[3] and r[3] != 'None': d['info'] = r[3]
    d['ref'] = r[4]
    d['alt'] = r[5]
    return json.dumps(d)


def _get_variant_set_method_1():
    """This is kind of hacky.  Got this idea from
    github.com/achave11/brca-exchange/website/django/data/views.py .
    Probably doesn't work, but gives us an idea."""
    SETNAME = 'someone-variants'
    DATASET_ID = 'someone'
    REFERENCE_SET_BASE = 'someone'
    import google.protobuf.json_format as json_format
    from ga4gh import variants_pb2 as variants
    dataset, id_ = variant_set_id.split('-')
    variant_set = variants.VariantSet()
    variant_set.id = '{}-{}'.format(dataset, id_)
    variant_set.name = '{}-{}'.format(SETNAME, id_)
    #variant_set.dataset_id = DATASET_ID
    #variant_set.reference_set_id = '{}-{}'.format(REFERENCE_SET_BASE, id_)
    return json_format._MessageToJsonObject(variant_set, True)
def _get_variant_set_method_2():
    """This method relies on using the vcf_id field of the 'variants'
    table. The theory is that we can compute the correct variant set via
    the distinct values for this field from each row."""
    import subprocess, json
    c = "gemini query -q 'select distinct vcf_id from variants' %s" % DATABASE_LOCATION
    r = subprocess.check_output(c, shell=True).split()
    return json.dumps(len(r))
def get_variant_set(variant_set_id):
    """It's easy enough, if the GA4GH API provides a standard get-on-ID
    operation, and thankfully Gemini already simply has a table called
    'variants' with which you can 'get' based on ID."""
    return _get_variant_set_method_2()


def search_call_sets(body):
    return 'do some magic!'

def search_variant_sets(body):
    return 'do some magic!'

def search_variants(body):
    return 'do some magic!'

def get_call_set(callSetId):
    return 'do some magic!'
