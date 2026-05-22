package mop;

import org.aspectjml.lang.annotation.siesta.Before;

/**
 * Warns if a ServerSocket object is constructed with an invalid backlog
 * value.
 *
 * The backlog argument must be a positive value greater than 0. If the value
 * passed if equal or less than 0, then the default value will be assumed.
 * http://docs.oracle.com/javase/6/docs/api/java/net/ServerSocket.html#ServerSocket%28int,%20int%29
 *
 * @severity warning
 */

public class ServerSocket_BacklogHandler {

    @Before("* java.net.ServerSocket+.bind(..)")
    public static void vioServerSocket_BacklogBind(String name, boolean isStatic, Object[] args){
      eventServerSocket_Backlog(args);
    }
    @Before("java.net.ServerSocket.new(..)")
    public static void vioServerSocket_BacklogNew(String name, boolean isStatic, Object[] args){
    	eventServerSocket_Backlog(args);
    }
	
	public void eventServerSocket_Backlog(int backlog) {
		if(backlog <= 0) {
			LoggerSpecification.printLogging(SpecificationType.ServerSocket_Port, null);
		}
	}
}
