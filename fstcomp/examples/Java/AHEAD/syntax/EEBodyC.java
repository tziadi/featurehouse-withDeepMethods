// Automatically generated code.  Edit at your own risk!
// Generated by bali2jak v2002.09.03.



public class EEBodyC extends EEBody {

    final public static int ARG_LENGTH = 2 ;
    final public static int TOK_LENGTH = 1 /* Kludge! */ ;

    public EqExprChoices getEqExprChoices () {
        
        return (EqExprChoices) arg [0] ;
    }

    public InstanceOfExpression getInstanceOfExpression () {
        
        return (InstanceOfExpression) arg [1] ;
    }

    public boolean[] printorder () {
        
        return new boolean[] {false, false} ;
    }

    public EEBodyC setParms (EqExprChoices arg0, InstanceOfExpression arg1) {
        
        arg = new AstNode [ARG_LENGTH] ;
        tok = new AstTokenInterface [TOK_LENGTH] ;
        
        arg [0] = arg0 ;            /* EqExprChoices */
        arg [1] = arg1 ;            /* InstanceOfExpression */
        
        InitChildren () ;
        return (EEBodyC) this ;
    }

}
