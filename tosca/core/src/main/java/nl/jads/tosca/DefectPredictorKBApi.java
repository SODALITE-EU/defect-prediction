package nl.jads.tosca;

import kb.dto.Attribute;
import kb.dto.Feature;
import kb.dto.Property;
import kb.repository.KB;
import kb.utils.MyUtils;
import kb.utils.QueryUtil;
import nl.jads.tosca.dto.BugRecord;
import nl.jads.tosca.dto.BugReport;
import nl.jads.tosca.dto.Comment;
import nl.jads.tosca.dto.FindBugInput;
import org.eclipse.rdf4j.model.IRI;
import org.eclipse.rdf4j.model.Value;
import org.eclipse.rdf4j.query.BindingSet;
import org.eclipse.rdf4j.query.TupleQueryResult;
import org.eclipse.rdf4j.query.impl.SimpleBinding;
import org.eclipse.rdf4j.repository.RepositoryConnection;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class DefectPredictorKBApi {

    public static String DCTERMS = "http://purl.org/dc/terms/";
    public static String DUL = "http://www.loa-cnr.it/ontologies/DUL.owl#";
    public static String TOSCA = "https://www.sodalite.eu/ontologies/tosca/";
    public static String SODA = "https://www.sodalite.eu/ontologies/sodalite-metamodel/";
    String PREFIXES = "PREFIX tosca: <https://www.sodalite.eu/ontologies/tosca/> \r\n" +
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\n" +
            "PREFIX soda: <https://www.sodalite.eu/ontologies/sodalite-metamodel/> \r\n" +
            "PREFIX DUL: <http://www.loa-cnr.it/ontologies/DUL.owl#> \r\n" +
            "PREFIX dcterms: <http://purl.org/dc/terms/> \r\n" +
            "PREFIX owl: <http://www.w3.org/2002/07/owl#> \r\n";
    private KB kb;

    public DefectPredictorKBApi(KB kb) {
        this.kb = kb;
    }

    public static void main(String[] args) throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(new KB());
        FindBugInput findBugInput = new FindBugInput();
        BugReport bugReport = kbApi.findBugs(findBugInput);
        for (BugRecord r : bugReport.getBugs()) {
            System.out.println(r.getBugName());
            System.out.println(r.getBugInfo().serialise());
        }
    }

    public void shutDown() {
        if (kb != null) {
            kb.shutDown();
        }
    }

    public Set<Attribute> getAllAttributes(RepositoryConnection connection) throws IOException {
        Set<Attribute> attributes = new HashSet<>();
        String sparql = MyUtils.fileToString("sparql/getAllAttributes.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection, query);

        while (result.hasNext()) {
            BindingSet bindingSet = result.next();
            IRI attr = (IRI) bindingSet.getBinding("attribute").getValue();
            IRI concept = (IRI) bindingSet.getBinding("concept").getValue();
            Value _value = bindingSet.hasBinding("value") ? bindingSet.getBinding("value").getValue() : null;

            Attribute a = new Attribute(attr);
            a.setClassifiedBy(concept);
            if (_value != null)
                a.setValue(_value, kb);

            attributes.add(a);
        }
        result.close();
        return attributes;
    }

    public Set<Property> getProperties(RepositoryConnection connection) throws IOException {
        Set<Property> properties = new HashSet<>();
        String sparql = MyUtils.fileToString("sparql/getAllProperties.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection, query);

        while (result.hasNext()) {
            BindingSet bindingSet = result.next();
            IRI p1 = (IRI) bindingSet.getBinding("property").getValue();
            IRI concept = (IRI) bindingSet.getBinding("concept").getValue();
            Value _value = bindingSet.hasBinding("value") ? bindingSet.getBinding("value").getValue() : null;

            Property a = new Property(p1);
            a.setClassifiedBy(concept);
            if (_value != null)
                a.setValue(_value, kb);

            properties.add(a);
        }
        result.close();
        return properties;
    }

    public boolean adminByDefault(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/adminByDefault.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean emptyPassword(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/emptyPassword.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean hardcodedSecret(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/hardcodedSecret.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean invalidIPAddressBinding(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/invalidIPAddressBinding.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean useOfHTTPWithoutTLS(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/useOfHTTPwithoutTLS.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean weakCryptoAlgo(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/weakCryptoAlgo.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public List<Comment> suspiciousComment(RepositoryConnection connection) throws IOException {
        String sparql = MyUtils.fileToString("sparql/suspiciousComment.sparql");
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
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

    public BugReport findBugs(FindBugInput bugInput) throws IOException {
        RepositoryConnection connection = kb.getConnection();
        BugReport bugReport = new BugReport();
        List<BugRecord> bugs = new ArrayList<>();
        for (Comment c : suspiciousComment(connection)) {
            if (c.getParameters() == null) {
                c.setParameters(new HashSet<>());
            }
            BugRecord bugRecord = new BugRecord();
            bugRecord.setBugName("SuspiciousComment");
            bugRecord.setBugInfo(c);
            bugs.add(bugRecord);
        }
        Set<Property> parameters = getProperties(connection);
        for (Property p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (adminByDefault(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("AdminByDefault");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (emptyPassword(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("EmptyPassword");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (hardcodedSecret(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("HardcodedSecret");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (invalidIPAddressBinding(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("InvalidIPAddressBinding");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (useOfHTTPWithoutTLS(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("UseOfHTTPWithoutTLS");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (weakCryptoAlgo(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("WeakCryptoAlgo");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
        }
        Set<Attribute> attributes = getAllAttributes(connection);
        for (Attribute p : attributes) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (adminByDefault(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("AdminByDefault");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (emptyPassword(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("EmptyPassword");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (hardcodedSecret(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("HardcodedSecret");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (invalidIPAddressBinding(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("InvalidIPAddressBinding");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (useOfHTTPWithoutTLS(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("UseOfHTTPWithoutTLS");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (weakCryptoAlgo(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("WeakCryptoAlgo");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
        }
        bugReport.setActionId(bugInput.getActionId());
        bugReport.setDeploymentId(bugInput.getDeploymentId());
        bugReport.setBugs(bugs);
        return bugReport;
    }
}
