import click
from plone_restapi_harvester.harvester.harvester import load_document, harvest_document
from plone_restapi_harvester.loaders.loaders import FSLoader


@click.command()
@click.argument(
    "input",
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    type=click.Path(exists=False),
)
def main(input, output):
    document_loader = FSLoader()
    normalized = harvest_document(load_document(document_loader, input))

    if output is not None:
        with open(output, "w") as fp:
            fp.write(normalized)
    else:
        print(normalized)


if __name__ == "__main__":
    # sys.exit(main())  # pragma: no cover
    main()
