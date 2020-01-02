package nl.jads.tosca;

import kb.KBApi;
import kb.dto.Attribute;
import kb.dto.Property;
import kb.utils.MyUtils;
import kb.utils.QueryUtil;
import org.eclipse.rdf4j.model.IRI;
import org.eclipse.rdf4j.model.Value;
import org.eclipse.rdf4j.query.BindingSet;
import org.eclipse.rdf4j.query.TupleQueryResult;
import org.eclipse.rdf4j.query.impl.SimpleBinding;
import nl.jads.tosca.dto.Comment;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class DefectPredictorKBApi extends KBApi {

    String PREFIXES = "PREFIX tosca: <https://www.sodalite.eu/ontologies/tosca/> \r\n" +
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\n" +
            "PREFIX soda: <https://www.sodalite.eu/ontologies/sodalite-metamodel/> \r\n" +
            "PREFIX DUL: <http://www.loa-cnr.it/ontologies/DUL.owl#> \r\n" +
            "PREFIX dcterms: <http://purl.org/dc/terms/> \r\n" +
            "PREFIX owl: <http://www.w3.org/2002/07/owl#> \r\n";

    public static String DCTERMS = "http://purl.org/dc/terms/";
    public static String DUL = "http://www.loa-cnr.it/ontologies/DUL.owl#";
    public static String TOSCA = "https://www.sodalite.eu/ontologies/tosca/";
    public static String SODA = "https://www.sodalite.eu/ontologies/sodalite-metamodel/";

    public DefectPredictorKBApi() {
        super();
    }

    public void shutDown() {
        super.shutDown();
    }

    public Set<Attribute> getAllAttributes() throws IOException {
        Set<Attribute> attributes = new HashSet<>();
        String sparql = MyUtils.fileToString("sparql/getAllAttributes.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(), query);

        while (result.hasNext()) {
            BindingSet bindingSet = result.next();
            IRI attr = (IRI) bindingSet.getBinding("attribute").getValue();
            IRI concept = (IRI) bindingSet.getBinding("p").getValue();

            Attribute a = new Attribute(attr);
            a.setClassifiedBy(concept);

            attributes.add(a);
        }
        result.close();
        return attributes;
    }

    public Set<Property> getProperties() throws IOException {
        Set<Property> properties = new HashSet<>();
        String sparql = MyUtils.fileToString("sparql/getAllProperties.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(), query);

        while (result.hasNext()) {
            BindingSet bindingSet = result.next();
            IRI p1 = (IRI) bindingSet.getBinding("property").getValue();
            IRI concept = (IRI) bindingSet.getBinding("concept").getValue();
            Value _value = bindingSet.hasBinding("value") ? bindingSet.getBinding("value").getValue() : null;

            Property a = new Property(p1);
            a.setClassifiedBy(concept);
            if (_value != null)
                a.setValue(_value, this);

            properties.add(a);
        }
        result.close();
        return properties;
    }

    public boolean adminByDefault(Property property) throws IOException {
        String sparql = MyUtils.fileToString("sparql/adminByDefault.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean emptyPassword(Property property) throws IOException {
        String sparql = MyUtils.fileToString("sparql/emptyPassword.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean hardcodedSecret(Property property) throws IOException {
        String sparql = MyUtils.fileToString("sparql/hardcodedSecret.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean invalidIPAddressBinding(Property property) throws IOException {
        String sparql = MyUtils.fileToString("sparql/invalidIPAddressBinding.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean useOfHTTPWithoutTLS(Property property) throws IOException {
        String sparql = MyUtils.fileToString("sparql/useOfHTTPwithoutTLS.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean weakCryptoAlgo(Property property) throws IOException {
        String sparql = MyUtils.fileToString("sparql/weakCryptoAlgo.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public List<Comment> suspiciousComment() throws IOException {
        String sparql = MyUtils.fileToString("sparql/suspiciousComment.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(kb.getConnection(),
                query);
        List<Comment> comments = new ArrayList<>();
        while (result.hasNext()) {
            BindingSet bindingSet = result.next();
            IRI p1 = (IRI) bindingSet.getBinding("resource").getValue();
            comments.add(new Comment(p1, bindingSet.getValue("comment").stringValue()));
        }
        result.close();
        return comments;
    }
    
    public static void main(String[] args) throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi();
        kbApi.suspiciousComment();

    }
}
