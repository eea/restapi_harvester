import click
import sys
from plone_restapi_harvester.harvester.harvester import load_document, harvest_document
from plone_restapi_harvester.loaders.loaders import FSLoader, PostgresLoader

@click.command()
@click.option('--loader', type=click.Choice(['fs', 'db']), default='fs')
@click.argument('id')
def main(id, loader):
    if loader == 'db':
        document_loader = PostgresLoader()
    else:
        document_loader = FSLoader() 
    import pdb;pdb.set_trace()
    normalized =  harvest_document(load_document(document_loader, id))    
    # pass data to the next airflow step
    a = 1

if __name__ == '__main__':
    #sys.exit(main())  # pragma: no cover
    main()