package mop;

import org.aspectjml.lang.annotation.siesta.Before;
import java.util.*;

/**
 * Warns if the destination list of Arrays.copy() is not as long as the source
 * list.
 *
 * Collections.copy() requires that the destination list be as long as the
 * source list.
 * http://docs.oracle.com/javase/6/docs/api/java/util/Collections.html#copy%28java.util.List,%20java.util.List%29
 *
 * This property checks the lengths of two lists.
 *
 * @severity error
 */

public class Collections_CopySizeHandler {

    @Before("* java.util.Collections.copy(..)")
    public static void vioCollections_CopySize(String name, boolean isStatic, Object[] args){
    	
       if (dest.size() < origen.size()) {
			LoggerSpecification.printLogging(SpecificationType.Collections_CopySize);
		}
    }
}
