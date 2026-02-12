package mop;

import org.aspectjml.lang.annotation.siesta.Before;

/**
 * Warns when the argument to decode is wrong
 *
 * According to the manual, the argument cannot contain any whitespace.
 * Also, there is a format to follow.
 * http://docs.oracle.com/javase/6/docs/api/java/lang/Long.html#decode%28java.lang.String%29
 *
 * @severity error
 */

public class Long_BadDecodeArgHandler {

    @Before("* java.lang.Long.decode(..)")
    public static void vioLong_BadDecodeArg(String name, boolean isStatic, Object[] args){

        Long_BadDecodeArgEvent(args);
    }
	public void Long_BadDecodeArgEvent(Long integer, String str) {

		if (str != null && str.length() != 0) {
			for(int i = 0; i < str.length(); ++i) {
				if (Character.isWhitespace(str.charAt(i))) {
					LoggerSpecification.printLogging(SpecificationType.Integer_BadDecodeArg);
				}
			}

			String substr;
			if (str.charAt(0) == '-') {
				substr = str.substring(1);
			} else {
				substr = str;
			}

			byte radix;
			if (!substr.startsWith("0x") && !substr.startsWith("0X")) {
				if (substr.startsWith("#")) {
					substr = substr.substring(1);
					radix = 16;
				} else if (substr.startsWith("0")) {
					substr = substr.substring(1);
					radix = 8;
				} else {
					radix = 10;
				}
			} else {
				substr = substr.substring(2);
				radix = 16;
			}

			try {
				if (Integer.parseInt(substr, radix) < 0L) {
					LoggerSpecification.printLogging(SpecificationType.Integer_BadDecodeArg);	
				}
			} catch (Exception e) {
				LoggerSpecification.printLogging(SpecificationType.Integer_BadDecodeArg);	
			}

		}else {
			LoggerSpecification.printLogging(SpecificationType.Integer_BadDecodeArg);	
		}

	}
}
