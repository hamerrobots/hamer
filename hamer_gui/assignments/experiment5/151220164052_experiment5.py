#!/usr/bin/env python
#Problem 1.a
#Problem 1.b
#Problem 1.c
#Problem 1.d
#Problem 1.d.1
import rospy
from geometry_msgs.msg import Twist
from math import fabs
#Problem 1.d.2
def patrol():
    #Problem 1.d.3
    rospy.init_node('patrol',anonymous=True)
    pub=rospy.Publisher('/hamer/cmd_vel',Twist,queue_size=10)
    #Problem 1.d.4
    move=Twist()
    #Problem 1.d.5
    vel=0.4
    dist=3
    cnt=0
    #Problem 1.d.6
    while cnt<10:
        t0=rospy.Time.now().to_sec()
        tr_dist=0.0
        if cnt %2==0:
            move.linear.x=vel
        else:
            move.linear.x=-vel
    	while tr_dist<dist:
        	pub.publish(move)
        	t1=rospy.Time.now().to_sec()
        	tr_dist=fabs(vel*t1-vel*t0)
	move.linear.x=0
	pub.publish(move)
	cnt+=1
    #Problem 1.d.7
    rospy.is_shutdown()
    #Problem 1.e
if __name__=='__main__':
    try:
        patrol()
    except rospy.ROSInterruptException:
        pass
#Problem 2
