from math import *


def controlleur(xd,yd,theta,x,y):
    x_thilde=xd-x
    y_thilde=yd-y
    theta_thilde = atan2(y_thilde,x_thilde)-theta
    d = sqrt(x_thilde^2+y_thilde^2)
    k1=0.7
    v=(k1*d)/cos(theta_thilde)
    k2=1.3
    if d<0.05 :
        w=(v/0.05)*sin(theta_thilde)+k2*theta_thilde
    else  :
        w=(v/d)*sin(theta_thilde)+k2*theta_thilde
    Ks=0.06
    L=0.0615
    pwm_g = (v-w*L)/Ks
    pwm_d = (v+w*L)/Ks
    if pwm_g>100:
        pwm_g=100
    if pwm_d>100:
        pwm_d=100
    if pwm_g<-100:
        pwm_g=-100
    if pwm_d<-100:
        pwm_d=-100
    return(pwm_g,pwm_d)

