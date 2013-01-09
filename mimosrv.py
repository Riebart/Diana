#!/usr/bin/env python

# Source: http://code.activestate.com/recipes/531824/

import select
import socket
import sys
import signal
import thread
import threading
import traceback


# ==============================================================================
# This implements sending serializable objects back and forth. We won't use it
# but this is kept around for fun

#import cPickle
#import struct

#marshall = cPickle.dumps
#unmarshall = cPickle.loads

#def send(channel, *args):
    #buf = marshall(args)
    #value = socket.htonl(len(buf))
    #size = struct.pack("L",value)
    #channel.send(size)
    #channel.send(buf)

#def receive(channel):
    #size = struct.calcsize("L")
    #size = channel.recv(size)
    #try:
        #size = socket.ntohl(struct.unpack("L", size)[0])
    #except struct.error, e:
        #return ''

    #buf = ""

    #while len(buf) < size:
        #buf = channel.recv(size - len(buf))

    #return unmarshall(buf)[0]

# ==============================================================================

# ==============================================================================

class MIMOServer:
    # ======================================================================

    class ThreadServer(threading.Thread):
        def __init__(self, server):
            threading.Thread.__init__(self)
            self.server = server

        def run(self):
            self.server.serve()

    # ======================================================================
    # ======================================================================

    class ThreadSocket(threading.Thread):
        def __init__(self, client, handler, event, on_hangup):
            threading.Thread.__init__(self)
            self.client = client
            self.handler = handler
            self.event = event
            self.on_hangup = on_hangup
            self.running = 1

        def run(self):
            while self.running:
                self.event.wait()
                if not self.running:
                    break

                try:
                    data = self.client.recv(1, socket.MSG_PEEK)
                    if not data:
                        break
                except socket.error, (errno, errstr):
                    if self.client.fileno() >= -1:
                        break

                    print "There was an error peeking at client %d" % self.client.fileno()
                    print "Error:", sys.exc_info()
                    sys.stdout.flush()
                    break

                #print "reading from %d" % self.client.fileno()
                #sys.stdout.flush()

                self.handler(self.client)
                self.event.clear()

            sys.stdout.flush()
            self.event.clear()
            self.on_hangup(self.client)

        def stop(self):
            self.running = 0
            self.event.set()

    # ======================================================================

    def __init__(self, callback, port=5505, backlog=5):
        self.running = 0
        self.port = port
        self.backlog = backlog
        self.callback = callback

        self.contextmap = dict()
        self.threadmap = dict()
        self.eventmap = dict()
        self.inputs = []
        self.hangup_lock = threading.Lock()
        self.hangups = []

        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        self.stop()

    def start(self):
        if self.running == 0:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(('', self.port))
            print 'Listening to port', self.port, '...'
            self.server.listen(self.backlog)
            self.inputs = [self.server]
            self.running = 1

            self.serve_thread = MIMOServer.ThreadServer(self)
            self.serve_thread.start()

    def stop(self):
        if self.running == 1:
            print "Shutting down server..."
            sys.stdout.flush()
            self.server.close()
            self.running = 0
            self.serve_thread.join()

            stubborn = 0
            while len(self.inputs) > 1:
                print "Hanging up %d %sclient%s" % (len(self.inputs) - 1,
                                                    "stubborn " if stubborn == 1 else "",
                                                    "s" if len(self.inputs) > 2 else "")
                for c in self.inputs:
                    if c != self.server:
                        self.hangup(c)
                stubborn = 1

            self.hangups = []

    # This gets called by a client's thread just before it terminates to tell us
    # that the client hung up
    def on_hangup(self, client):
        self.hangup_lock.acquire()
        self.hangups.append(client)
        self.hangup_lock.release()

    # This gets called when a client hangs up on us.
    def hangup(self, client):
        if client.fileno() == -1:
            # Detect an already hung-up client
            return

        self.threadmap[client].stop()
        client.close()

        self.inputs.remove(client)
        del self.threadmap[client]
        del self.contextmap[client]
        del self.eventmap[client]

    def serve(self):
        while self.running:
            try:
                inputready, outputready, exceptready = select.select(self.inputs, [], [])
            except select.error, e:
                print e
                break
            except socket.error, e:
                print e
                break
                
            if not self.running:
                break

            if len(self.hangups) > 0:
                self.hangup_lock.acquire()
                
                for h in self.hangups:
                    self.hangup(h)

                self.hangups = []
                    
                self.hangup_lock.release()
                continue

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    #print 'got connection %d from %s' % (client.fileno(), address)
                    sys.stdout.flush()

                    context = self.callback(client)
                    self.contextmap[client] = context
                    self.eventmap[client] = threading.Event()
                    self.threadmap[client] = MIMOServer.ThreadSocket(client, context.handle, self.eventmap[client], self.on_hangup)
                    self.threadmap[client].start()

                    self.inputs.append(client)

                elif not self.eventmap[s].is_set():
                    self.eventmap[s].set()

# ==============================================================================

class Tester:
    def __init__(self, client):
        self.client = client

    def handle(self, client):
        print "handling %d" % client.fileno()
        sys.stdout.flush()
        print client.recv(1024)

def cb(client):
    return Tester(client)

if __name__ == "__main__":
    srv = MIMOServer(cb)
    srv.start()
    raw_input("Press Enter to continue...\n")
    srv.stop()
    #raw_input("Press Enter to continue...\n")
    #srv.start()
    #raw_input("Press Enter to continue...\n")
    #srv.stop()
