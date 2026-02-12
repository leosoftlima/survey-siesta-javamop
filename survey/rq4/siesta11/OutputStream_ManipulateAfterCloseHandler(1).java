package mop;

import org.aspectjml.lang.annotation.siesta.Before;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;

/**
 * Warns write() or flush() after close().
 *
 * According to the OutputStream.close(), a closed stream cannot perform
 * output operations and cannot be reopened in general.
 * http://download.oracle.com/javase/6/docs/api/java/io/OutputStream.html#close%28%29
 *
 * ByteArrayOutputStream is an exceptional subclass in that methods in this
 * class can be called after the stream has been closed.
 * http://docs.oracle.com/javase/6/docs/api/java/io/ByteArrayOutputStream.html#close%28%29
 *
 * @severity error
 */

public class OutputStream_ManipulateAfterCloseHandler {

    @Before("* java.io.OutputStream+.close()")
    public static void vioOutputStream_ManipulateAfterClose(OutputStream  outputStream, String[] history){

        if(!(outputStream instanceof ByteArrayOutputStream)){
            outputStream_ManipulateAfterCloseEvent(history);
        }
    }
 public void outputStream_ManipulateAfterCloseEvent(String[] history) {

        String[] interesting = new String[] {"write", "flush"};
        if (filter(history, interesting)) {
            LoggerSpecification.printLogging(SpecificationType.OutputStream_ManipulateAfterClose);
        }

    }

    private boolean filter(String[] history, String[] interesting) {
        boolean foundClose = false;
        for (int i = 0; i < history.length; i++) {
            if ("close".equals(history[i])) {
                foundClose = true;
                // Verifica se há algum método interessante após o "close"
                for (int j = i + 1; j < history.length; j++) {
                    for (String interestingMethod : interesting) {
                        if (interestingMethod.equals(history[j])) {
                            return true;
                        }
                    }
                }
            }
        }
        return false;
    }
}
