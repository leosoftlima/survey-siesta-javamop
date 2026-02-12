package mop;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.PipedInputStream;
import java.io.PushbackInputStream;

import org.aspectjml.lang.annotation.siesta.Before;

/**
 * Prevents invocations of mark() if the InputStream does not support.
 *
 * Some subclasses of InputStream do not support mark() and reset().
 * http://download.oracle.com/javase/6/docs/api/java/io/InputStream.html#reset%28%29
 *
 * FileInputStream, PushbackInputStream, ObjectInputStream, PipedInputStream
 * and SequenceInputStream do not support mark() and reset(). This
 * specification warns if mark() or reset() is invoked. Users tend to assume
 * that OpenJDK implementation will always raise an exception if a stream does
 * not support mark(), but this is not guaranteed. In fact,
 * PushbackInputStream.mark() does nothing.
 *
 * @severity error
 */
public class InputStream_MarkResetHandler {

	@Before("* java.io.InputStream+.mark(..)")
	@Before("* java.io.InputStream+.reset(..)")
	public static void vioInputStream_MarkReset(String name, boolean isStatic, Object[] args) {
		if(hasElements(args)) {
			InputStream inputStream = 	(InputStream) args[0];
			if((inputStream instanceof FileInputStream) || 
					(inputStream instanceof PushbackInputStream) || 
					(inputStream instanceof ObjectInputStream) || 
					(inputStream instanceof PipedInputStream)){
                
				LoggerSpecification.printLogging(SpecificationType.InputStream_MarkReset);
			}
		}
	}

	private static boolean hasElements(Object[] args) {
		for (int i = 0; i < args.length; i++) {
			if(args[i] !=null)
				return true;
		}
		return false;
	}

}
