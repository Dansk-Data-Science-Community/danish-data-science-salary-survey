'''Unit tests for the data module'''

import pytest
from src.data import load_data


class TestData:
    '''Test the data module'''

    @pytest.fixture(scope='class')
    def df(self):
        yield load_data()

    def test_no_consent_column(self, df):
        '''Check that the consent column has been removed'''
        consent_col = "Do you agree to take part in this survey?"
        assert consent_col not in df.columns

    def test_column_names(self, df):
        '''Check that the column names are correct'''
        col_names = ['timestamp',
                     'salary',
                     'bonus',
                     'received_equity',
                     'job_title',
                     'num_employees',
                     'num_subordinates',
                     'sector',
                     'region',
                     'educational_background',
                     'highest_education',
                     'years_experience',
                     'gender',
                     'danish_national',
                     'uses_high_level_language',
                     'uses_mid_level_language',
                     'uses_visualisation_tools',
                     'uses_deployment_tools',
                     'uses_version_control',
                     'uses_spreadsheets',
                     'uses_query_languages',
                     'uses_distributed_computing_tools',
                     'uses_monitoring_tools',
                     'uses_automl_tools',
                     'uses_rpa_tools']
        for col in col_names:
            assert col in df.columns

    def test_column_types(self, df):
        '''Check that the column types are correct'''
        col_types = dict(timestamp='datetime64[ns, UTC]',
                         salary='int',
                         bonus='int',
                         received_equity='category',
                         job_title='category',
                         num_employees='category',
                         num_subordinates='category',
                         sector='category',
                         region='category',
                         educational_background='category',
                         highest_education='category',
                         years_experience='int',
                         gender='category',
                         danish_national='category',
                         uses_high_level_language='bool',
                         uses_mid_level_language='bool',
                         uses_visualisation_tools='bool',
                         uses_deployment_tools='bool',
                         uses_version_control='bool',
                         uses_spreadsheets='bool',
                         uses_query_languages='bool',
                         uses_distributed_computing_tools='bool',
                         uses_monitoring_tools='bool',
                         uses_automl_tools='bool',
                         uses_rpa_tools='bool')
        for col_name, dtype in df.dtypes.iteritems():
            assert col_types[col_name] == dtype
