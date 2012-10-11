import java.io.FileInputStream;
import java.io.FileNotFoundException;

import org.junit.Test;

import tmp.generated_java15.Java15Parser;
import cide.gparser.OffsetCharStream;
import cide.gparser.ParseException;
import de.ovgu.cide.fstgen.ast.FSTNonTerminal;

public class JavaParserTest {
	@Test
	public void runParser() throws FileNotFoundException, ParseException, tmp.generated_java15java15_withDeepMethods.ParseException {
		tmp.generated_java15java15_withDeepMethods.Java15Parser p = new tmp.generated_java15java15_withDeepMethods.Java15Parser(new FileInputStream("test/Test.java"));
		p.CompilationUnit(false);
		System.out.println(p.getRoot().printFST(0));
		tmp.generated_java15java15_withDeepMethods.SimplePrintVisitor s = new tmp.generated_java15java15_withDeepMethods.SimplePrintVisitor();
	    s.visit((FSTNonTerminal) p.getRoot());
	}
}
