package mop;

import org.aspectj.lang.JoinPoint;
import org.aspectjml.lang.annotation.After;

/**
 * Warns if a class is runnable without overriding run() method.
 *
 * According to the manual, runnable class must provide its own run() method.
 * http://docs.oracle.com/javase/6/docs/api/java/lang/Runnable.html
 *
 * @severity error
 */
public class Runnable_OverrideRunHandler {

    @After("staticinitialization(java.lang.Runnable+)")
    public static void vioRunnable_OverrideRun(JoinPoint joinPoint) {
       Class objClasse = joinPoint.getStaticPart().getSignature().getDeclaringType();
       Runnable_OverrideRunEvent(objClasse);
    }
	 private String[] getMethodRunnable_OverrideRun(Class<?> klazz) {
	        if (klazz != null) {
	            try {
	                Method method = klazz.getMethod("run");
	                if (method != null && method.getName().equals("run")) {
	                    return new String[]{"run"}; 
	                }
	            } catch (NoSuchMethodException e) {
	                e.printStackTrace();
	            }
	        }
	        return null; 
	    }
	 
	 public void Runnable_OverrideRunEvent(Class<?> klazz) {
	   String [] methodRun= getMethodRunnable_OverrideRun(klazz);
		 
		if (methodRun !=null) {
		    if(!methodRun[0].equals("run")) {
		    	LoggerSpecification.printLogging(SpecificationType.Authenticator_OverrideGetPasswordAuthentication);
		    }
		}
	 }
}
