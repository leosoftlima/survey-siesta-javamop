package mop;

import org.aspectjml.lang.annotation.siesta.Before;
import java.util.PriorityQueue;

/**
 * Warns if PriorityQueue is about to have a non-comparable object.
 *
 * PriorityQueue does not permit non-comparable elements.
 * http://docs.oracle.com/javase/6/docs/api/java/util/PriorityQueue.html
 *
 * The definition of a non-comparable object is not clear, but it is assumed
 * that an object that does not implement the Comparable interface is deemed
 * to be non-comparable.
 *
 * @severity error
 */

public class PriorityQueue_NonComparableHandler {

    @Before("* java.util.PriorityQueue.add*(..)")
    @Before("* java.util.Queue+.offer*(..)")
    public static void vioPriorityQueue_NonComparableAdd(String name, boolean isStatic, Object[] args){
    	Object o = args[1];
        eventPriorityQueue_NonComparableAdd(o);
    }

    @Before("* java.util.Collection+.addAll(java.util.Collection)")
    public static void vioPriorityQueue_NonComparableaddAll(PriorityQueue priorityQueue){
    	eventPriorityQueue_NonComparableAddAll(priorityQueue);
    }
	
	public void eventPriorityQueue_NonComparableAdd(Object o) {
		if(!(o instanceof Comparable)) {
			LoggerSpecification.printLogging(SpecificationType.PriorityQueue_NonComparable);
		}
	}
	
    public void eventPriorityQueue_NonComparableAddAll(PriorityQueue<Object> objects) {
	   	for (Object o : objects) {
	   		if(!(o instanceof Comparable)) {
				LoggerSpecification.printLogging(SpecificationType.PriorityQueue_NonComparable);
			}
		}
	}
}
