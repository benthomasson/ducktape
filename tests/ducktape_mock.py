# Copyright 2015 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ducktape.cluster.cluster import Cluster
from ducktape.tests.session import SessionContext
from ducktape.tests.test import TestContext
from ducktape.cluster.remoteaccount import RemoteAccount, RemoteAccountSSHConfig
from mock import MagicMock


import os
import tempfile


def mock_cluster():
    return MagicMock()


class FakeCluster(Cluster):
    """A cluster class with counters, but no actual node objects"""
    def __init__(self, num_nodes):
        self._num_nodes = num_nodes
        self._available_nodes = self._num_nodes

    def __len__(self):
        return self._num_nodes

    def alloc(self, nslots):
        """Request the specified number of slots, which will be reserved until they are freed by the caller."""
        self._available_nodes -= nslots
        return [object() for _ in range(nslots)]

    def num_available_nodes(self):
        return self._available_nodes

    def free(self, slots):
        self._available_nodes += len(slots)

    def free_single(self, _):
        self._available_nodes += 1


def session_context(**kwargs):
    """Return a SessionContext object"""

    if "results_dir" not in kwargs.keys():
        tmp = tempfile.mkdtemp()
        session_dir = os.path.join(tmp, "test_dir")
        os.mkdir(session_dir)
        kwargs["results_dir"] = session_dir

    return SessionContext(session_id="test_session", **kwargs)


def test_context(session_context=session_context(), cluster=mock_cluster()):
    """Return a TestContext object"""
    return TestContext(session_context=session_context, file="a/b/c", cluster=cluster)


class MockNode(object):
    """Mock cluster node"""
    def __init__(self):
        self.account = MockAccount()


class MockAccount(RemoteAccount):
    """Mock node.account object"""
    def __init__(self):

        ssh_config = RemoteAccountSSHConfig(
            host="localhost",
            user=None,
            hostname="localhost",
            port=22)

        super(MockAccount, self).__init__(ssh_config, externally_routable_ip="localhost", logger=None)
