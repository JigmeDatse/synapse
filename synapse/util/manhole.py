# Copyright 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.conch.manhole import ColoredManhole
from twisted.conch.insults import insults
from twisted.conch import manhole_ssh
from twisted.cred import checkers, portal


from twisted.internet import reactor


def listen_manhole(bind_address, bind_port, username, password, globals):
    """Starts a ssh listener with password authentication using
    the given username and password. Clients connecting to the ssh
    listener will find themselves in a colored python shell with
    the supplied globals.

    Args:
        bind_address(str): IP address to listen on.
        bind_port(int): TCP port to listen on.
        username(str): The username ssh clients should auth with.
        password(str): The password ssh clients should auth with.
        globals(dict): The variables to expose in the shell.
    """

    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(
        **{username: password}
    )

    rlm = manhole_ssh.TerminalRealm()
    rlm.chainedProtocolFactory = lambda: insults.ServerProtocol(
        ColoredManhole,
        dict(globals, __name__="__console__")
    )

    factory = manhole_ssh.ConchFactory(portal.Portal(rlm, [checker]))

    reactor.listenTCP(bind_port, factory, interface=bind_address)