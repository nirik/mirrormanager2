# -*- coding: utf-8 -*-

'''
mirrormanager2 model tests.
'''

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

import mirrormanager2.lib
import mirrormanager2.lib.model as model
import tests


class MMLibModeltests(tests.Modeltests):
    """ Model tests. """

    def test_mirrormanagerbasemixin(self):
        """ Test the MirrorManagerBaseMixin object of
        mirrormanager2.lib.model.
        """
        tests.create_base_items(self.session)

        item = model.Arch.get(self.session, 1)
        self.assertEqual(item.name, 'source')
        item = model.Arch.get(self.session, 3)
        self.assertEqual(item.name, 'x86_64')

    def test_site_repr(self):
        """ Test the Site.__repr__ object of mirrormanager2.lib.model.
        """
        tests.create_site(self.session)

        item = model.Site.get(self.session, 1)
        self.assertEqual(str(item), '<Site(1 - test-mirror)>')
        item = model.Site.get(self.session, 3)
        self.assertEqual(str(item), '<Site(3 - test-mirror_private)>')

    def test_host_repr(self):
        """ Test the Host.__repr__ object of mirrormanager2.lib.model.
        """
        tests.create_site(self.session)
        tests.create_hosts(self.session)

        item = model.Host.get(self.session, 1)
        self.assertEqual(str(item), '<Host(1 - mirror.localhost)>')
        item = model.Host.get(self.session, 3)
        self.assertEqual(str(item), '<Host(3 - private.localhost)>')

    def test_host_json(self):
        """ Test the Host.__json__ object of mirrormanager2.lib.model.
        """
        tests.create_site(self.session)
        tests.create_hosts(self.session)

        item = model.Host.get(self.session, 1)
        self.assertEqual(
            item.__json__(),
            {
                'admin_active': True,
                'asn': None,
                'asn_clients': False,
                'bandwidth_int': 100,
                'comment': None,
                'country': u'US',
                'id': 1,
                'internet2': False,
                'internet2_clients': False,
                'last_checked_in': None,
                'last_crawl_duration': 0,
                'last_crawled': None,
                'max_connections': 10,
                'name': u'mirror.localhost',
                'private': False,
                'site': {'id': 1, 'name': u'test-mirror'},
                'user_active': True
            }
        )
        item = model.Host.get(self.session, 3)
        self.assertEqual(
            item.__json__(),
            {
                'admin_active': True,
                'asn': None,
                'asn_clients': False,
                'bandwidth_int': 100,
                'comment': 'My own private mirror',
                'country': u'NL',
                'id': 3,
                'internet2': False,
                'internet2_clients': False,
                'last_checked_in': None,
                'last_crawl_duration': 0,
                'last_crawled': None,
                'max_connections': 10,
                'name': u'private.localhost',
                'private': True,
                'site': {'id': 1, 'name': u'test-mirror'},
                'user_active': True
            }
        )

    def test_host_set_not_up2date(self):
        """ Test the Host.set_not_up2date object of mirrormanager2.lib.model.
        """
        tests.create_site(self.session)
        tests.create_hosts(self.session)
        tests.create_base_items(self.session)
        tests.create_directory(self.session)
        tests.create_category(self.session)
        tests.create_hostcategory(self.session)
        tests.create_hostcategorydir(self.session)

        item = model.Host.get(self.session, 1)
        # Before change, all is up2date
        for hc in item.categories:
            for hcd in hc.directories:
               self.assertTrue(hcd.up2date)

        item.set_not_up2date(self.session)

        # After change, all is *not* up2date
        for hc in item.categories:
            for hcd in hc.directories:
               self.assertFalse(hcd.up2date)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MMLibModeltests)
    unittest.TextTestRunner(verbosity=10).run(SUITE)
