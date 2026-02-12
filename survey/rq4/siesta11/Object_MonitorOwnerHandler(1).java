package mop;

import org.aspectjml.lang.annotation.siesta.Before;

public class Object_MonitorOwnerHandler {

    @Before("* java.lang.Object+.wait(..)")
    public static void vioObject_MonitorOwnerWait(String name, boolean isStatic, Object[] args){
        Object o = (Object) args[0];
        if(!Thread.holdsLock(o)){
           eventObject_MonitorOwnerNotify(args);
        }
    }

    @Before("* java.lang.Object+.notifyAll(..)")
    @Before("* java.lang.Object+.notify(..)")
    public static void vioObject_MonitorOwnerNotify(String name, boolean isStatic, Object[] args){
        Object o = (Object) args[0];
        if(!Thread.holdsLock(o)){
           eventObject_MonitorOwnerNotify(args);
        }
    }
	
	public void eventObject_MonitorOwnerWait(Object o) {
		LoggerSpecification.printLoggingObject_MonitorOwner(2);
	}
	
	public void eventObject_MonitorOwnerNotify(Object o) {
		LoggerSpecification.printLoggingObject_MonitorOwner(1);
	}
}
