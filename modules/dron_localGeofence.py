import threading
import time


def _inGeofence (self, position = None):
    if position == None:
        position = self.position

    if abs(position[0]) < self.localGeofence[0] // 2 and \
        abs(position[1]) < self.localGeofence[1] // 2 and \
        position[2] < self.localGeofence[2] and position[2] > 0:
            return True
    else:
            return False



def setLocalGeofence (self, dimN_S, dimE_O, altura):
    # el geofence local se define en términos de las dimensiones
    # del espacio, es este orden: Norte-sur, Este-oeste, altura

    self.localGeofence = [dimN_S, dimE_O, altura]

def _localGeofenceCheck (self):

    while self.localGeofenceEnabled:
        if self.state == 'flying':
            if not self._inGeofence():
                if self.localGeofenceBreachAction == 2:
                    self.Land(blocking = False)
                elif self.localGeofenceBreachAction == 3:
                    self.RTL (blocking = False)
                if self.localGeofenceBreachCallback != None:
                    if self.id == None:
                        if  self.localGeofenceBreachCallbackParams == None:
                            self.localGeofenceBreachCallback()
                        else:
                            self.localGeofenceBreachCallback( self.localGeofenceBreachCallbackParams)
                    else:
                        if  self.localGeofenceBreachCallbackParams == None:
                            self.localGeofenceBreachCallback(self.id)
                        else:
                            self.localGeofenceBreachCallback(self.id,  self.localGeofenceBreachCallbackParams)

        time.sleep (0.25)


def enableLocalGeofence (self, callback = None, params = None):
    self.localGeofenceEnabled = True
    self.localGeofenceBreachCallback = callback
    self.localGeofenceBreachCallbackParams = params

    localGoefenceCheckThread = threading.Thread(target=self._localGeofenceCheck)
    localGoefenceCheckThread.start()
    self.localGeofenceChecking = True

def disableLocalGeofence (self):
    self.localGeofenceEnabled = False

def setLocalGeofenceBreachAction (self,action):
    self.localGeofenceBreachAction = action

def startLocalGeofenceChecking (self):
    self.localGeofenceChecking = True

def stopLocalGeofenceChecking (self):
    self.localGeofenceChecking = False
