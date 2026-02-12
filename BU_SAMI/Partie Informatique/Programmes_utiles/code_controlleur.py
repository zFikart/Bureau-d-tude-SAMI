from math import *


def controlleur(xd,yd,theta,x,y):
    """
    en argumant : positions de départ et arrivée
    x : position robot
    x_d : position désirée
    x_thilde : erreur position
    k1 gain 1
    k2 gain 2
    """
    Ks = 0.06
    k1 = 0.7
    k2 = 1.3
    L = 0.0615
    "erreur de position"
    x_thilde=xd-x
    y_thilde=yd-y
    theta_thilde = atan2(y_thilde,x_thilde)-theta

    "distance d'erreur de position"
    d = (x_thilde^2 + y_thilde^2)**(1/2)

    ""
    v = (k1*d) / cos(theta_thilde


    "condition pour vitesse de rotation des roues"
    if d<0.05 :
        w = (v/0.05)*sin(theta_thilde) + k2*theta_thilde
    else:
        w = (v/d)*sin(theta_thilde) + k2*theta_thilde

    "Gains statique et "
    

    "expression du pwm"
    pwm_g = (v-w*L)/Ks
    pwm_d = (v+w*L)/Ks

    "condition bizarre genre pour donner les max"
    if pwm_g > 100:
        pwm_g = 100
    if pwm_d > 100:
        pwm_d = 100
    if pwm_g < -100:
        pwm_g = -100
    if pwm_d < -100:
        pwm_d = -100

    return(pwm_g,pwm_d)

