import json
import requests

KNOWN_BLOCK_DATA_TYPES = {
    "eeametadata/geocoverage": {
        "metadata": "geo_coverage_countries",
        "mappings": [{"key": "value", "type": "list", "mapTo": ""}],
    }
}


def load_document(document_loader, document_id):
    """
    Get document from document_loader. document_loader class must provide a read method
    which gets a document id and returns a json serializable string based on plone.restapi
    response
    """
    raw_doc = document_loader.read(document_id)
    return json.loads(raw_doc)


def get_blocks_list(data):
    """ get all available blocks in a given JSON provided Plone REST API. Return a list of blocks """
    blocks_to_return = []
    if "blocks" in data:
        blocks = data.get("blocks")
        if isinstance(blocks, dict):
            # when blocks is a dict, each dict item represents a different block
            # so we return it and inspect if it has additional blocks
            for key, block in blocks.items():
                blocks_to_return.append(block)

            blocks_to_return.extend(get_blocks(block))

        elif isinstance(blocks, list):
            # when blocks is a list, each item is in itself a block
            for block in blocks:
                blocks_to_return.append(block)

            blocks_to_return.extend(get_blocks(block))

    return blocks_to_return


def get_blocks_from_dict(block):
    yield block

    for value in block.values():
        yield from get_blocks(value)


def get_blocks(data):
    """ get all available blocks in a given JSON provided Plone REST API. Return a generator"""
    if isinstance(data, dict):
        if "blocks" in data:
            blocks = data.get("blocks")
            if isinstance(blocks, dict):
                # when blocks is a dict, each key represents a different block
                # so we return it and inspect if it has additional blocks
                for key, block in blocks.items():
                    yield from get_blocks_from_dict(block)

                yield from get_blocks(block)

            elif isinstance(blocks, list):
                # when blocks is a list, each item is in itself a block
                for block in blocks:
                    yield from get_blocks_from_dict(block)

                yield from get_blocks(block)

def extract_data(block):
    """
    Check block for known types of data
    """
    normalized_data = {}
    mappings = KNOWN_BLOCK_DATA_TYPES.get(block.get('@type'), {}).get('mappings')
    metadata = KNOWN_BLOCK_DATA_TYPES.get(block.get('@type'), {}).get('metadata')
    for mapping in mappings:
        if mapping.get('mapTo'):
            current = normalized_data.get(metadata, {})
            current[mapping.get('mapTo')] = block.get(mapping.get('key'),'')
            normalized_data[metadata] = current
        else:
            normalized_data[metadata] = block.get(mapping.get('key'),'')
    return normalized_data
    
def get_default_data(document):
    """
    Extract default plone content type metadata
    """
    normalized_data = {}
    normalized_data["title"] = document.get("title")
    normalized_data["description"] = document.get("description")
    normalized_data["abstract"] = document.get("abstract")
    normalized_data["created"] = document.get("creation_date")
    normalized_data["published"] = document.get("effectiveDate")
    normalized_data["expires"] = document.get("expirationDate")
    return normalized_data

def extract_metadata_from_api(document):
    """
    Check @metadata endpoint. This enpoint must return a mapping from document screma to
    output JSON key
    """
    normalized_data = {}
    metadata_endpoint = document.get("@components", {}).get("@metadata", {}).get("@id")
    mapping_response = metadata_endpoint and requests.get(metadata_endpoint)
    if mapping_response is not None and mapping_response.status_code == 200:
        for k,v in mapping_response.json().get('items', {}):
            normalized_data[k] = document.get(v)
    return normalized_data

def harvest_document(document):
    """
    1. Harvest plone default data
    2. Check @metadata endpoint
    3. Discover block metadata
    """
    data = get_default_data(document)
    data.update(extract_metadata_from_api(document))
    block_list = get_blocks(document)
    for block in block_list:
        if block.get('@type') in KNOWN_BLOCK_DATA_TYPES:
            data.update(extract_data(block))
    return data