# -*- coding: utf-8 -*-
#
# Copyright © 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
MirrorManager2 internal api.
'''

import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

from mirrormanager2.lib import model


def create_session(db_url, debug=False, pool_recycle=3600):
    ''' Create the Session object to use to query the database.

    :arg db_url: URL used to connect to the database. The URL contains
    information with regards to the database engine, the host to connect
    to, the user and password and the database name.
      ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg debug: a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a Session that can be used to query the database.

    '''
    engine = sqlalchemy.create_engine(
        db_url, echo=debug, pool_recycle=pool_recycle)
    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


def get_mirrors(
        session, private=None, internet2=None, internet2_clients=None,
        asn_clients=None, admin_active=None, user_active=None):
    ''' Retrieve the mirrors based on the criteria specified.

    :arg session: the session with which to connect to the database.

    '''
    query = session.query(
        model.Host
    ).order_by(
        model.Host.country
    )

    if private is not None:
        query = query.filter(model.Host.private == private)
    if internet2 is not None:
        query = query.filter(model.Host.internet2 == internet2)
    if internet2_clients is not None:
        query = query.filter(model.Host.internet2_clients == internet2_clients)
    if asn_clients is not None:
        query = query.filter(model.Host.asn_clients == asn_clients)
    if admin_active is not None:
        query = query.filter(model.Host.admin_active == admin_active)
    if user_active is not None:
        query = query.filter(model.Host.user_active == user_active)

    return query.all()