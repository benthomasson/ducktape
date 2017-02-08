# Copyright 2016 Confluent Inc.
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

from ducktape.tests.test import Test


class TestLoggingConfig(Test):

    def test_logging_config(self):
        expected_config = {('debug_log', 'ServiceX'): "on fail",
                           ('info_log', 'ServiceX'): True,
                           ('error_log', 'ServiceX'): True}

        assert expected_config == self.test_context.log_collect
