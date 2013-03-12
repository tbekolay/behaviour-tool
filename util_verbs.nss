#include "z_verbs"

/* CallForHelp verb
Description: oSubject calls for help
VerbData Arguments: oSubject
Verb Arguments:
    string sLine [Mandatory] - The line oSubject calls out.
*/
void CallForHelp(struct verbData vData, string sLine);

/* FaceAndSayLine verb
Description: oSubject faces oDirObject and says sLine
VerbData Arguments: oSubject oDirObject
Verb Arguments:
    string sLine [Mandatory] - The line oSubject says.
*/
void FaceAndSayLine(struct verbData vData, string sLine);

/* Fight verb
Description: oSubject attacks oDirObject
VerbData Arguments: oSubject oDirObject
*/
void Fight(struct verbData vData);

/* FocusOnActor verb
Description: oSubject becomes the center of attention through camera moves.
VerbData Arguments: oSubject
*/
void FocusOnActor(struct verbData vData);

/* PlotKill verb
Description: oSubject is killed as part of some plot; the body sticks around until it is expressly destroyed
VerbData Arguments: oSubject
*/
void PlotKill(struct verbData vData);

/* RunAwayFrom verb
Description: oSubject runs away from oDirObject
VerbData Arguments: oSubject oDirObject
*/
void RunAwayFrom(struct verbData vData);

/* RunTowards verb
Description: oSubject runs towards oDirObject
VerbData Arguments: oSubject oDirObject
*/
void RunTowards(struct verbData vData);

/* SayLine verb
Description: oSubject says sLine
VerbData Arguments: oSubject
Verb Arguments:
    string sLine [Mandatory] - The line oSubject says.
*/
void SayLine(struct verbData vData, string sLine);

/* SayLineWithAction verb
Description: oSubject says sLine and plays the passed animation
VerbData Arguments: oSubject
Verb Arguments:
    string sLine [Mandatory] - The line oSubject says.
    int nAnimation [Mandatory] - NWScript constant representing the animation
    float fSpeed [Optional] - The speed at which the animation plays (relative to the default, 1.0)
    float fDurationSeconds [Optional] - How long a looping animation will play
*/
void SayLineWithAction(struct verbData vData, string sLine, int nAnimation, float fSpeed=1.0, float fDurationSeconds=0.0);

/* StartConversation verb
Description: oSubject starts sConversation with oDirObject
VerbData Arguments: oSubject oDirObject
Verb Arguments:
    string sConversation [Mandatory] - The conversation to be started
*/
void StartConversation(struct verbData vData, string sConversation);

/* WalkAwayFrom verb
Description: oSubject walks from oDirObject
VerbData Arguments: oSubject oDirObject
*/
void WalkAwayFrom(struct verbData vData);

/* WalkRandomly verb
Description: oSubject walks randomly for a while
VerbData Arguments: oSubject
*/
void WalkRandomly(struct verbData vData);

/* WalkTowards verb
Description: oSubject walks towards oDirObject
VerbData Arguments: oSubject oDirObject
*/
void WalkTowards(struct verbData vData);