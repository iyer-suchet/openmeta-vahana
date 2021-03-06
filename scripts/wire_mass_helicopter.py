'''
# Name: wire_mass_helicopter.py
# Company: MetaMorph, Inc.
# Author(s): Joseph Coombe
# Email: jcoombe@metamorphsoftware.com
# Create Date: 6/20/2017
# Edit Date: 6/20/2017

# Conversion of Airbus A^3's vahanaTradeStudy>reserveMission.mat code
# (located here: https://github.com/VahanaOpenSource/vahanaTradeStudy )
# to Python 2.7 for use in the MetaMorph, Inc. OpenMETA environment
# http://www.metamorphsoftware.com/openmeta/

# Helicopter Configuration Only: Estimate wire mass including DC power cables and communications cables

# Inputs:
#   span            - wingspan [m]
#   fuselageLength  - fuselage length [m]
#   fuselageHeight  - fuselage height [m]
#   power           - maximum DC power draw [W]
#   xMotor          - motor locations [m]

# Outputs:
#   mass            - estimated wire mass [kg]
'''

from __future__ import print_function

from openmdao.api import Component
import numpy as np
import math

class wire_mass(Component):
    def __init__(self):
        super(wire_mass, self).__init__()
        self.add_param('span', val=0.0)
        self.add_param('fuselageLength', val=0.0)
        self.add_param('fuselageHeight', val=0.0)
        self.add_param('power', val=0.0)
        self.add_param('xmotor', val=0.0)
        
        self.add_output('mass', val=0.0)
    
    def solve_nonlinear(self, params, unknowns, resids):
        # In the future, xmotor should be a parameter array that gets passed in from the outside
        xmotor = params['xmotor']
        
        nMotors = 1
        
        # Power Cables
        P = params['power']/nMotors
        cableDensity = 1e-5 # Approximate power cable pair density [kg/m/W], ~500 g/m for pair of wires carrying 50 kW
        
        # Wires for each motor runs half fuselage length and height on average. Also runs out from center to location on wing.  
        L = nMotors * params['fuselageLength'] / 2.0 + nMotors * params['fuselageHeight'] / 2.0 + 0.0 * params['span'] / 2.0
        massCables = cableDensity * P * L
        
        # Sensor Wires
        wireDensity = 0.0046 # kg/m
        wiresPerBundle = 6 # Wires per bundle
        L = L + 10.0 * params['fuselageLength'] + 4.0 * params['span'] # Additional wires for motor controllers, airdata, lights, servos, sensors
        massWires = 2.0 * wireDensity * wiresPerBundle * L # Sensor wires for motors
        
        unknowns['mass'] = massCables + massWires