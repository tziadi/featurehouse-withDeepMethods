// Automatically generated code.  Edit at your own risk!
// Generated by bali2jak v2002.09.03.



public class IoExpr extends InstanceOfExpression {

    final public static int ARG_LENGTH = 2 ;
    final public static int TOK_LENGTH = 1 ;

    public AST_TypeName getAST_TypeName () {
        
        return (AST_TypeName) arg [1] ;
    }

    public RelationalExpression getRelationalExpression () {
        
        return (RelationalExpression) arg [0] ;
    }

    public boolean[] printorder () {
        
        return new boolean[] {false, true, false} ;
    }

    public IoExpr setParms
    (RelationalExpression arg0, AstToken tok0, AST_TypeName arg1) {
        
        arg = new AstNode [ARG_LENGTH] ;
        tok = new AstTokenInterface [TOK_LENGTH] ;
        
        arg [0] = arg0 ;            /* RelationalExpression */
        tok [0] = tok0 ;            /* "instanceof" */
        arg [1] = arg1 ;            /* AST_TypeName */
        
        InitChildren () ;
        return (IoExpr) this ;
    }

}
