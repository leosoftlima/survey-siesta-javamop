package mop;

import org.aspectjml.lang.annotation.siesta.Before;
import java.net.DatagramPacket;

/**
 * Warns if DatagramPacket.setLength() is called with an invalid length.
 *
 * According to the reference of DatagramPacket.setLength(), the length, a
 * parameter of DatagramPacket.setLength(), must be lesser or equal to the
 * offset plus the length of the packet's buffer.
 * http://docs.oracle.com/javase/6/docs/api/java/net/DatagramPacket.html#setLength%28int%29
 *
 * It is considered that the explanation is incorrect. It seems the offset
 * plus the new length must be lesser or equal to the length of the packet's
 * buffer. This property is based on this interpretation.
 *
 * @severity error
 */
public class DatagramPacket_SetLengthHandler {

    @Before("void java.net.DatagramPacket.setLength(int)")
    public static void vioDatagramPacket_SetLength(DatagramPacket datagramPacket, int length ){
       EventDatagramPacket_SetLength(datagramPacket, length);
    } 
	public void EventDatagramPacket_SetLength(DatagramPacket datagramPacket ,int length ) {
		 int offset = datagramPacket.getOffset();
		    byte[] buffer = datagramPacket.getData();

		    if (length + offset > buffer.length) {
		    	LoggerSpecification.printLogging(SpecificationType.DatagramPacket_SetLength, String.valueOf(length), String.valueOf(offset), String.valueOf(buffer.length));
		    }
	}
}
