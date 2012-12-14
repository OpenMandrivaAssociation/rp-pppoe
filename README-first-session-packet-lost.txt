First session packet lost

SHORT PROBLEM DESCRIPTION
ADSL connection takes too long on some network: the first PPP negotiation 
packet from the server is lost, thus requiring a retransmit after a timeout.

DETAILED PROBLEM DESCRIPTION
Some PPPoE server will start PPP negotiation very few usec after they have sent
the last packet of PPPoE discovery (PADS).
In the Linux implementation of PPPoE, using low level packet sockets, 
initialization of the specific socket for PPPoE session traffic can take a non 
negligible amount of time. In general, executing in user mode, no assumption 
can be made on timings.
Packets arriving to the Ethernet driver before the socket for the PPPoE session
protocol is created will be lost.
This can lead to delays in the PPP connection, since the server will wait for a 
given period a reply to its first negotiation packet, retransmitting it after a 
timeout period.
In the case observed the timeout was 20sec, increasing abnormally the time for 
ADSL connection, that requires no more than 1-2sec on WinXP.

SOLUTION
The solution implemented in this patch is to open the session socket before the 
discovery phase ends.
Thus every session packet arriving after the PADS packet, no matter how fast,
will be buffered by the packet socket layer.

IMPLEMENTATION
Discovery and session phase initialization are handled in these files:
pppoe.c
	session() - initialization of session phase
plugin.c
	PPPOEConnectDevice() - initialization of communication for kernel-level
                               PPPoE
discovery.c
	discovery() - initialization of discovery phase
In order to anticipate the creation of the session socket, while leaving
the initialization functionalities encapsulated in the functions discovery()
and session(), my choice was to:
1 - bring the creation of socket out of discovery() and session()
2 - create the session socket before the invocation of discovery(), both in
    session() and PPPOEConnectDevice()
While this is not optimal in terms of behavior (in fact the best place for
creating the session socket would be after sending the PADR packet and before
receiving of PADS packet in discovery()) it looks cleaner, while requiring a
minimum intervention on the code.
Taking the creation of the discovery socket out of discovery() does not have
functional reasons, but preserves symmetricity between the functions.

Luigi Sgro
luigi.sgro@tiscali.it
