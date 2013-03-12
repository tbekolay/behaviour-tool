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

import re
import Codegen

class ParseError(Exception):
    """An exception raised by the parsing functions when the input script is not well-formed."""
    def __init__(self, value):
        """Sets up the instance variable."""
        self.value = value
        """A message passed by the function raising the error.
        @type: string
        """
    def __str__(self):
        """Generate a string representation of the error.
        @return: The value passed to the error when it was raised.
        @rtype: string
        """
        return repr(self.value)

def ParseVerbs(script):
    """Parses the C{util_verbs.nss} script to generate a list of ActualVerbs.
    @param script: The entirety of the C{util_verbs.nss} script.
    @type script: list of strings
    @return: The ActualVerbs described in the C{util_verbs.nss} script.
    @rtype: list of L{ActualVerb}s
    """

    # Set up the list
    actual_verbs = []
    
    # Regular expressions to parse the verb comments.
    name_re = re.compile(r"/\* (?P<name>\w+) verb")
    description_re = re.compile(r"Description: (?P<description>.*)")
    vdarguments_re = re.compile(r"VerbData Arguments: (?P<vdargs>.*)")
    varguments_re = re.compile(r"Verb Arguments:")
    vargument_re = re.compile(r"    (?P<type>\w+) (?P<name>\w+) (?P<mandatory>\S+) - (?P<description>.*)")
    
    # Make a list of line #'s that contain /*; each will identify a verb.
    lines = []
    
    for ix, line in enumerate(script):
        if line.find("/*") != -1:
            lines.append(ix)
    
    # Parse each verb's comment block.
    for ix in lines:
        # /* <Verb name> verb
        match_object = name_re.match(script[ix])
        
        if match_object is None:
            continue
        verb = Codegen.ActualVerb()
        verb.name = match_object.group("name")

        # Description: <Verb description>
        match_object = description_re.match(script[ix+1])
        
        if match_object is None:
            continue
        verb.description = match_object.group("description")
        
        # VerbData Arguments: <vdarguments separated by spaces>
        match_object = vdarguments_re.match(script[ix+2])
        
        if match_object is None:
            continue
        vdargs = match_object.group("vdargs")
        vdargs_list = vdargs.split()
        for vdarg in vdargs_list:
            verb.vdarguments.append(vdarg)
        
        # Verb Arguments:
        match_object = varguments_re.match(script[ix+3])
        
        if match_object is not None:
            # Find the line containing '*/'
            start_ix = end_ix = ix+4
            while script[end_ix].find("*/") == -1:
                end_ix += 1
            
            # Go through each verb argument
            for v_ix in range(end_ix - start_ix):
                #     <type> <name> <mandatory> - <description>
                match_object = vargument_re.match(script[start_ix+v_ix])
                
                if match_object is None:
                    continue
                
                mandatory = match_object.group("mandatory") == "[Mandatory]"
                type = match_object.group("type")
                name = match_object.group("name")
                description = match_object.group("description")
                
                verb.varguments.append((mandatory, type, name, description))

        # If we're here, we'll assume our parsing worked out,
        # so add this actual verb to the list.
        actual_verbs.append(verb)
    
    return actual_verbs

def ParseBehaviour(script):
    """Parses the behaviour script to generate a behaviour object.
    @param script: The entirety of the C{b_<behaviour>.nss} script.
    @type script: list of strings
    @return: The behaviour object able to generate the passed script.
    @rtype: L{Behaviour}
    @raise ParseError: Raised if the script's opening comment block is malformed;
        if the comment markers do not line up, or a verb attempts to be manipulated
        before it is declared.
    """

    # Set up the behaviour object that we'll eventually return
    out_behaviour = Codegen.Behaviour()

    # Regular expressions that will be used to parse the opening comment block.
    behaviour_re = re.compile(r"BEHAVIOUR: (?P<name>\w+)")
    verb_re = re.compile(r"VERB\d+: (?P<context_name>\w+) (?P<actual_name>\w+) (?P<follower>\w+) ?(?P<terminal>\w*)")
    actor_re = re.compile(r"ACTOR\d+: (?P<type>\w+) (?P<name>\w+) (?P<description>.*)")
    nwvar_re = re.compile(r"VARIABLE\d+: (?P<type>\w+) (?P<name>\w+) (?P<description>.*)")

    verb_preconditions_re = re.compile(r"    VERB(?P<id>\d+)_PRECONDITIONS: (?P<preconds>.*)")
    verb_followers_re = re.compile(r"    VERB(?P<id>\d+)_FOLLOWERS: (?P<followers>.*)")
    verb_verbdata_re = re.compile(r"    VERB(?P<id>\d+)_VERBDATA: (?P<vdargs>.*)")
    verb_arguments_re = re.compile(r"    VERB(?P<id>\d+)_ARGUMENTS: (?P<vargs>.*)")

    # Find the first comment block
    for ix, line in enumerate(script):
        if line.find("/*") != -1:
            start_block = ix
            break

    for ix, line in enumerate(script):
        if line.find("*/") != -1:
            end_block = ix
            break

    # Skip over the lines that don't contain useful information
    start_block += 2

    if start_block > end_block:
        raise ParseError, "Error parsing the opening comment block!"

    # Since we won't know about all the verbs until we have finished parsing,
    # we'll keep a list of the follower relationships in memory until we have
    # finished parsing, then use the list afterwards to fill in the objects.
    all_followers = []

    # Get the info we want from the opening comment block.
    for ix in range(end_block - start_block):
        line = script[start_block + ix]

        # BEHAVIOUR: <name>
        match_object = behaviour_re.match(line)
        if match_object is not None:
            out_behaviour.name = match_object.group("name")
            continue

        # VERBx: <context_name> <actual_name> <follower> <terminal>
        match_object = verb_re.match(line)
        if match_object is not None:
            new_verb = Codegen.Verb(out_behaviour)
            new_verb.context_name = match_object.group("context_name")
            new_verb.actual_name = match_object.group("actual_name")

            if match_object.group("follower") == "Follower":
                new_verb.follower = True
            else:
                new_verb.follower = False

            if match_object.group("terminal") == "Terminal":
                new_verb.terminal = True
            else:
                new_verb.terminal = False

            out_behaviour.verbs.append(new_verb)
            continue

        #     VERBx_PRECONDITIONS: <preconditions seperated by ;;>
        match_object = verb_preconditions_re.match(line)
        if match_object is not None:
            v_ix = int(match_object.group("id")) - 1
            preconds = match_object.group("preconds")
            preconds_list = preconds.split(";;")
            for precond in preconds_list:
                try:
                    out_behaviour.verbs[v_ix].preconditions.append(precond.strip(' ;'))
                except:
                    raise ParseError, "Verb not yet declared."
            continue

        #     VERBx_FOLLOWERS: <followers seperated by spaces>
        match_object = verb_followers_re.match(line)
        if match_object is not None:
            v_ix = int(match_object.group("id")) - 1
            followers = match_object.group("followers")
            followers_list = followers.split()
            for follower in followers_list:
                all_followers.append((new_verb.context_name, follower))
            continue

        #     VERBx_VERBDATA: <vdarguments seperated by spaces>
        match_object = verb_verbdata_re.match(line)
        if match_object is not None:
            v_ix = int(match_object.group("id")) - 1
            vdargs = match_object.group("vdargs")
            vdargs_list = vdargs.split()
            for vdarg in vdargs_list:
                try:
                    out_behaviour.verbs[v_ix].vdarguments.append(vdarg)
                except:
                    raise ParseError, "Verb not yet declared."
            continue

        #     VERBx_ARGUMENTS: <varguments seperated by ;;>
        match_object = verb_arguments_re.match(line)
        if match_object is not None:
            v_ix = int(match_object.group("id")) - 1
            vargs = match_object.group("vargs")
            vargs_list = vargs.split(";;")
            for varg in vargs_list:
                try:
                    out_behaviour.verbs[v_ix].varguments.append(varg.strip(' ;'))
                except:
                    raise ParseError, "Verb not yet declared."
            continue


        # ACTORx: <type> <name> <description>
        match_object = actor_re.match(line)
        if match_object is not None:
            out_behaviour.nwvariables.append(\
                Codegen.NWVariable(\
                    type=match_object.group("type"),\
                    name=match_object.group("name"),\
                    description=match_object.group("description"),\
                    isActor=True))
            continue

        # VARIABLEx: <type> <name> <description>
        match_object = nwvar_re.match(line)
        if match_object is not None:
            out_behaviour.nwvariables.append(\
                Codegen.NWVariable(\
                    type=match_object.group("type"),\
                    name=match_object.group("name"),\
                    description=match_object.group("description"),\
                    isActor=False))
            continue

        print "Unable to parse line:", line

    # After we've parsed the comment block, we'll run through our list of
    # follower relationships.
    for follow_pair in all_followers:
        for verb in out_behaviour.verbs:
            if verb.context_name == follow_pair[0]:
                v1 = verb
                break
        for verb in out_behaviour.verbs:
            if verb.context_name == follow_pair[1]:
                v2 = verb
                break
        
        v1.followers.append(v2)

    return out_behaviour
