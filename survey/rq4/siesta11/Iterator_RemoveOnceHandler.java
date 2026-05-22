package mop;

import org.aspectjml.lang.annotation.siesta.Before;
import java.util.Iterator;

/**
 * Warns if Iterator.remove() is called multiple times per next().
 *
 * Iterator.remove() can be called only once per call to next().
 * http://docs.oracle.com/javase/6/docs/api/java/util/Iterator.html#remove%28%29
 *
 * This property warns if remove() is not preceded by next().
 *
 * @severity error
 */

public class Iterator_RemoveOnceHandler {

    @Before("void java.util.Iterator+.remove()")
    public static void vioIterator_RemoveOnce(Iterator i, String[] history){

        eventIterator_RemoveOnce(history);
    }
	public void eventIterator_RemoveOnce(String[] history) {
		String[] interesting = new String[] {"next"};

			if(filter(history, interesting)  && !validate(history)) {
				LoggerSpecification.printLogging(SpecificationType.Iterator_RemoveOnce);
			}
	}
	private boolean validate(String[] history) {
		for (int i = 0; i < history.length; i++) {
			String string = history[i];
			if(history[i] !=null && equalshere(history[i] ,"listIterator")) {
				return true;
			}
		}
		return false;
	}
	
	private boolean filter(String[] history, String[] interesting) {
	    boolean foundRemove = false;
	    boolean foundNext = false;

	    for (String action : history) {
	        if (equalshere("remove",action)) {
	            if (foundRemove) {
	                return true; // Retorna true se encontrar dois "remove" consecutivos sem um "next" entre eles
	            }
	            foundRemove = true; // Marca que encontrou um "remove"
	        } else if (equalshere("next",action)) {
	            if (!foundRemove) {
	                foundNext = true; // Marca que encontrou um "next" sem um "remove" anterior
	            }else {
	            	foundNext = false;
	            }
	        }
	    }

	    // Retorna true se encontrar um único "remove" sem um "next" subsequente
	    return foundRemove && !foundNext;
	}


	private boolean equalshere(String str1, String str2) {
	    if (str1 == null || str2 == null) {
	        return false;
	    }
	    int n = str1.length();
	    if (n != str2.length()) {
	        return false;
	    }
	    char v1[] = str1.toCharArray();
	    char v2[] = str2.toCharArray();
	    for (int i = 0; i < n; i++) {
	        if (v1[i] != v2[i]) {
	            return false;
	        }
	    }
	    return true;
	}
}
