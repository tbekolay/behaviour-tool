# Copyright (c) 2010, Trevor Bekolay
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, this
#      list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this
#      list of conditions and the following disclaimer in the documentation and/or other
#      materials provided with the distribution.
#    * Neither the name of the IRCL nor the names of its contributors may be used to
#      endorse or promote products derived from this software without specific prior
#      written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os.path
import Parser

def LoadActualVerbs(path):
    """Loads and parses the C{util_verbs.nss} file.
    @param path: Path to the C{util_verbs.nss} file.
    @type path: string
    @return: A list containing the L{ActualVerb}s in the parsed file
    @rtype: list of L{ActualVerb}s
    @raise IOError: If the path points to a file not named
        C{util_verbs.nss}, an IOError will be raised.
    """
    if os.path.basename(path) != "util_verbs.nss":
        raise IOError, -1, "Filename must be 'util_verbs.nss'"
    
    FILE = open(path, 'r')
    script = FILE.readlines()
    FILE.close()
    
    # Get a list of ActualVerbs by parsing util_verbs
    actual_verbs = Parser.ParseVerbs(script)
    
    return actual_verbs

def LoadBehaviour(path):
    """Loads and parses a generated script file from disk.

    Note that we can generate a complete behaviour object from the b_ file,
    so we don't need to load the z_b_ file.
    @param path: Path to the C{b_<behaviour>.nss} file.
    @type path: string
    @return: The behaviour object defined in the script.
    @rtype: L{Behaviour}
    @raise IOError: If the path points to a file that does not begin with
        C{b_}, an IOError will be raised.
    """
    # Make sure we're working with a b_ file.
    if os.path.basename(path)[0:2] != "b_":
        raise IOError, -1, "Filename must start with b_"

    FILE = open(path, 'r')
    script = FILE.readlines()
    FILE.close()

    # Get a behaviour object by parsing the script
    out_behaviour = Parser.ParseBehaviour(script)

    return out_behaviour

def SaveBFile(path, behaviour):
    """Saves the b_ code generated from the passed behaviour to disk.
    @param path: Path where we would like to save the b_ code.
        This must begin with C{b_}.
    @type path: string
    @param behaviour: The beheaviour object we are generating code from.
    @type behaviour: L{Behaviour}
    @raise IOError: If the path points to a file that does not begin with
        C{b_}, an IOError will be raised.
    """
    # Make sure we're working with a b_ file.
    if os.path.basename(path)[0:2] != "b_":
        raise IOError, -1, "Filename must start with b_"
    
    FILE = open(path, 'w')
    FILE.write(behaviour.GenerateBCode())
    FILE.close()

def SaveZBFile(path, behaviour):
    """Saves the z_b_ code generated from the passed behaviour to disk.
    @param path: Path where we would like to save the z_b_ code.
        This must begin with C{z_b_}.
    @type path: string
    @param behaviour: The beheaviour object we are generating code from.
    @type behaviour: L{Behaviour}
    @raise IOError: If the path points to a file that does not begin with
        C{b_}, an IOError will be raised.
    """
    # Make sure we're working with a z_b_ file.
    if os.path.basename(path)[0:4] != "z_b_":
        raise IOError, -1, "Filename must start with z_b_"

    FILE = open(path, 'w')
    FILE.write(behaviour.GenerateZBCode())
    FILE.close()
