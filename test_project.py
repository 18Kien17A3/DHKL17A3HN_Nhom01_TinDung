"""Kiểm tra quy tắc dữ liệu, lọc và ba trang ứng dụng."""
import unittest
import pandas as pd
from analysis import load_data, kpis, grouped, filter_data, lookup, ASSETS

class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = load_data()

    def test_reconcile(self):
        d = self.df
        k = kpis(d)
        self.assertEqual((k['total'], k['approved'], k['rejected']), (4269,2656,1613))
        self.assertEqual(k['requested_amount'],64604700000)
        self.assertAlmostEqual(k['approval_rate'],2656/4269)
        self.assertEqual(d.loan_id.nunique(),len(d))

    def test_assets_not_invented(self):
        d = self.df
        self.assertEqual(d.asset_issue.sum(),28)
        self.assertEqual(d.residential_assets_value.isna().sum(),28)
        self.assertEqual(d.total_assets.isna().sum(),28)
        self.assertFalse(d[ASSETS].lt(0).any().any())
        self.assertEqual(d.loc[d.asset_issue,'residential_assets_value_raw'].unique().tolist(),[-100000])

    def test_group_denominator_and_lookup(self):
        g = grouped(self.df, 'cibil_band')
        self.assertEqual(g.total.sum(),4269)
        self.assertEqual(g.approved.sum(),2656)
        self.assertEqual(len(lookup(self.df,'CIBIL thấp nhưng được duyệt')),185)
        self.assertEqual(len(lookup(self.df,'CIBIL cao nhưng bị từ chối')),13)
        self.assertEqual(lookup(self.df,query='60,197').loan_id.tolist(),[60,197])
        self.assertTrue(lookup(self.df,query='không tồn tại').empty)
        self.assertTrue(lookup(self.df,'CIBIL thấp nhưng được duyệt',300).empty)

    def test_filters_and_empty(self):
        d=self.df
        out=filter_data(d,['Approved'],['Graduate','Not Graduate'],['Yes','No'],(300,900),(2,20),(200000,9900000))
        self.assertEqual(len(out),2656)
        self.assertEqual(kpis(out)['approval_rate'],1)
        out=filter_data(d,[],['Graduate'],['Yes'],(300,900),(2,20),(200000,9900000))
        self.assertTrue(out.empty)
        self.assertIsNone(kpis(out)['approval_rate'])

class AppTests(unittest.TestCase):
    def test_pages_search_reset_and_empty(self):
        from pathlib import Path
        from streamlit.testing.v1 import AppTest
        at=AppTest.from_file(str(Path(__file__).with_name('app.py')),default_timeout=40).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value,'4,269')
        at.radio[0].set_value('2. Phân tích chuyên sâu').run()
        self.assertFalse(at.exception)
        at.radio[0].set_value('3. Tra cứu hồ sơ').run()
        self.assertFalse(at.exception)
        at.selectbox(key='quick').set_value('Tài sản cần kiểm tra').run()
        self.assertEqual(len(at.dataframe[0].value),28)
        at.text_input(key='query').set_value('60').run()
        self.assertEqual(len(at.dataframe[0].value),1)
        at.text_input(key='query').set_value('abc').run()
        self.assertTrue(at.dataframe[0].value.empty)
        next(b for b in at.button if b.label=='Đặt lại bộ lọc').click().run()
        self.assertEqual(len(at.dataframe[0].value),4269)
        at.multiselect(key='status').set_value([]).run()
        self.assertFalse(at.exception)
        self.assertTrue(any('Không có hồ sơ' in x.value for x in at.info))

if __name__ == '__main__':
    unittest.main(verbosity=2)
