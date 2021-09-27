=================
restapi_harvester
=================


This python package takes care of providing the relevant indexing data of a given Plone site
using its REST API.

It uses a three-way strategy to harvest the data from Plone's REST API.

1. Extract the known metadata directly from known attributes

Some core metadata are saved under known attributes name in Plone. As Plone REST API provides
all attributes of a given Plone page in its response, this harvester extracts the following
known attributes directly from there:


+---------------++----------------+
| Metadata      | Plone attribute |
+===============+=================+
| title         | title     |
+---------------+-----------------+
| description   | description     |
+---------------+-----------------+
| abstract      | description     |
+---------------+-----------------+
| created       | created         |
+---------------+-----------------+
| published     | effective       |
+---------------+-----------------+
| expires       | expires         |
+---------------+-----------------+
| modified      | modified        |
+---------------+-----------------+
| absolute_url  | N/A (*)         |
+---------------+-----------------+
| UID           | UID             |
+---------------+-----------------+

(*) The absolute_url is not a proper Plone attribute, but it's calculated through the REST API.

2. Extract all metadata from the @metadata endpoint

When harvesting a Plone site developers may have established which metadata should be
indexed using `eea.api.coremetadata`_. This extension product for the Plone REST API
provides an adapter-based way to expose arbitrary metadata in an specific endpoint.

The harvester takes the values from that endpoint, if present, and returns them to
the indexer.

3. Extract Volto blocks

When using Volto to build the front-end of a Plone site, the end-user may have used
some specific Volto block types to expose some metadata without requiring the Plone
developers to expose that information through the REST API.

The harvester extracts the metadata present in some already known Volto block types
and exposes them to the indexer. Right now, only the values of *eeametadata/geocoverage*
block types are taken into account, but more can be included in the future.


.. _`eea.api.coremetadata`: https://github.com/eea/eea.api.coremetadata
