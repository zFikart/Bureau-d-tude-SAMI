from math import *


def controlleur(xd,yd,theta,x,y):
    x_thilde=xd-x
    y_thilde=yd-y
    theta_thilde = atan2(y_thilde,x_thilde)-theta

    d = sqrt(x_thilde^2+y_thilde^2)
    k1=0.7
    v=(k1*d)/cos(theta_thilde)
    k2=1.3
    Ks=0.06
    L=0.0615
    if d<0.05 :
        w=(v/0.05)*sin(theta_thilde)+k2*theta_thilde
    else  :
        w=(v/d)*sin(theta_thilde)+k2*theta_thilde
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
    return(pwm_g,pwm_d,d)



# l=[[],[],[],[]]
# for i in range(len(l)):
#     x,y, theta=
#     d=controlleur(l[i][0],l[i][1],theta,x,y)[2]
#     while d>0.05 :
#         x,y,theta =                                    #récupération coordonnées
#         pwm_g,pwmd=controlleur(l[0][0],l[0][1],theta,x,y)[0],controlleur(l[0][0],l[0][1],theta,x,y)[1]
#         vg,vd=pwm_g*Ks,pwm_d*Ks
#         time.sleep(0.02)
## voilà il y a vg et vd








