from .base import *
from .datasource import *

class DataSource(Resource):
    def download(self, target, overwrite=False):
        raise NotImplementedError

class URLDataSource(DataSource):
    def __init__(self, url):
        self.url = url
    
    def download(self, filename, **kwargs):
        import urllib.request
        return urllib.request.urlretrieve(self.get_url(), filename, **kwargs)

    def get_url(self) -> str:
        if hasattr(self, 'url'):
            return self.url
        else:
            return self.datasource.get_url()

    def to_dataflow(self) -> 'dprep.Dataflow':
        import azureml.dataprep as dprep
        return dprep.auto_read_file(self.get_url())

    def to_pandas_dataframe(self):
        return self.to_dataflow().to_pandas_dataframe()

    def to_spark_dataframe(self) -> 'pyspark.sql.DataFrame':
        return self.to_dataflow().to_spark_dataframe()

# TODO: can we auto-generate this type (or register for multiple yaml_tag?)
class CSVDataSource(URLDataSource):
    yaml_tag = u'!csv'
    def to_dataflow(self) -> 'dprep.Dataflow':
        import azureml.dataprep as dprep
        # dprep.read_json
        # TODO: lookup method dprep.read_*
        # not sure if the **self.get_params() is such a great idea as it ain't portable?
        return dprep.read_csv(self.get_url(),  **self.get_params('url'))