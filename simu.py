'''
Created on 19 Aug 2016

@author: romeokienzler
'''
from scipy.integrate import odeint
#import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, Response
import os
from cStringIO import StringIO


app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))



def Lorenz(state,t):
  # unpack the state vector
  x = state[0]
  y = state[1]
  z = state[2]

  # these are our constants
  sigma = 10.0
  rho = 28.0
  beta = 8.0/3.0

  # compute state derivatives
  xd = sigma * (y-x)
  yd = (rho-z)*x - y
  zd = x*y - beta*z

  # return the state derivatives
  return [xd, yd, zd]



# do some fancy 3D plotting
#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.plot(state[:,0],state[:,1],state[:,2])
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#ax.set_zlabel('z')
#plt.show()
#plt.plot(t, state[:,0])
#plt.xlabel('TIME (sec)')
#plt.ylabel('STATES')
#plt.title('Lorenz x')
#plt.plot(t, state[:,1])
#plt.xlabel('TIME (sec)')
#plt.ylabel('STATES')
#plt.title('Lorenz x')
#plt.plot(t, state[:,2])
#plt.xlabel('TIME (sec)')
#plt.ylabel('STATES')
#plt.title('Lorenz x')


@app.route('/')
def hello_world():
    state0 = [2.0, 3.0, 4.0]
    t = np.arange(0.0, 30.0, 0.01)

    state = odeint(Lorenz, state0, t)
    x = np.array(t)
    x.shape=(3000,1)
    returnValue = np.concatenate((x, state), axis=1)
    output = StringIO()
    np.savetxt(output, returnValue, delimiter=";",newline='\n')
    csv_string = output.getvalue()
    response = Response(csv_string, mimetype='text/csv')
    response.headers['Content-Disposition'] = u'attachment; filename=lorenz.csv'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
#
