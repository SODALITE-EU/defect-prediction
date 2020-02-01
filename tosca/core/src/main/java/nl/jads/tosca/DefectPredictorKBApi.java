package nl.jads.tosca;

import kb.dto.Attribute;
import kb.dto.Feature;
import kb.dto.Property;
import kb.repository.KB;
import kb.utils.QueryUtil;
import nl.jads.tosca.dto.BugRecord;
import nl.jads.tosca.dto.BugReport;
import nl.jads.tosca.dto.Comment;
import nl.jads.tosca.dto.FindBugInput;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.eclipse.rdf4j.model.IRI;
import org.eclipse.rdf4j.model.Value;
import org.eclipse.rdf4j.model.impl.SimpleLiteral;
import org.eclipse.rdf4j.query.Binding;
import org.eclipse.rdf4j.query.BindingSet;
import org.eclipse.rdf4j.query.TupleQueryResult;
import org.eclipse.rdf4j.query.impl.SimpleBinding;
import org.eclipse.rdf4j.repository.RepositoryConnection;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
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
    private String homeLoc;

    public DefectPredictorKBApi(KB kb) {
        this(kb, "");
    }

    public DefectPredictorKBApi(KB kb, String homeLoc) {
        this.kb = kb;
        this.homeLoc = homeLoc;
    }

    public static void main(String[] args) throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(new KB());
        FindBugInput findBugInput = new FindBugInput();
        BugReport bugReport = kbApi.findBugs(findBugInput);
        for (BugRecord r : bugReport.getBugs()) {
            System.out.println(r.getBugName());
            System.out.println(r.getContext());
            System.out.println(r.getElementName());
            System.out.println(r.getElementType());
//            System.out.println(r.getBugInfo().serialise());
        }
    }

    public void shutDown() {
        if (kb != null) {
            kb.shutDown();
        }
    }

    private String fileToString(String file) throws IOException {
        String path = homeLoc + file;
        InputStream inputStream;
        if (new File(path).exists()) {
            inputStream = FileUtils.openInputStream(new File(path));
        } else {
            inputStream = Thread.currentThread().getContextClassLoader().getResourceAsStream(file);
        }
        if (inputStream == null) {
            return null;
        }
        return IOUtils.toString(inputStream, StandardCharsets.UTF_8.name());
    }

    public Set<Attribute> getAllAttributes(RepositoryConnection connection) throws IOException {
        Set<Attribute> attributes = new HashSet<>();
        String sparql = fileToString("sparql/getAllAttributes.sparql");
        if (sparql == null) {
            return attributes;
        }
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
        String sparql = fileToString("sparql/getAllProperties.sparql");
        if (sparql == null) {
            return properties;
        }
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
        String sparql = fileToString("sparql/adminByDefault.sparql");
        if (sparql == null) {
            return false;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean emptyPassword(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/emptyPassword.sparql");
        if (sparql == null) {
            return false;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean hardcodedSecret(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/hardcodedSecret.sparql");
        if (sparql == null) {
            return false;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean invalidIPAddressBinding(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/invalidIPAddressBinding.sparql");
        if (sparql == null) {
            return false;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean useOfHTTPWithoutTLS(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/useOfHTTPwithoutTLS.sparql");
        if (sparql == null) {
            return false;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public boolean weakCryptoAlgo(Feature property, RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/weakCryptoAlgo.sparql");
        if (sparql == null) {
            return false;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", property.getClassifiedBy()));
        boolean tobeReturned = result.hasNext();
        result.close();
        return tobeReturned;
    }

    public List<Comment> suspiciousComment(RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/suspiciousComment.sparql");
        List<Comment> comments = new ArrayList<>();
        if (sparql == null) {
            return comments;
        }
        String query = PREFIXES + sparql;
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query);

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
            bugRecord.setDescription("The Comment contains suspicious information");
            fillContext(bugRecord, c, connection);
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
                bugRecord.setDescription("The default user is admin");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (emptyPassword(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("EmptyPassword");
                bugRecord.setDescription("The password is empty");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (hardcodedSecret(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("HardcodedSecret");
                bugRecord.setDescription("The password or user name is hardcoded");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (invalidIPAddressBinding(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("InvalidIPAddressBinding");
                bugRecord.setDescription("The address has a binding of 0.0.0./*L");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (useOfHTTPWithoutTLS(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("UseOfHTTPWithoutTLS");
                bugRecord.setDescription("The address uses HTTP without TSL");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (weakCryptoAlgo(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("WeakCryptoAlgo");
                bugRecord.setDescription("The cryptography algorithm is weak");
                fillContext(bugRecord, p, connection);
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
                bugRecord.setDescription("The default user is admin");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (emptyPassword(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("EmptyPassword");
                bugRecord.setDescription("The password is empty");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (hardcodedSecret(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("HardcodedSecret");
                bugRecord.setDescription("The password or user name is hardcoded");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (invalidIPAddressBinding(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("InvalidIPAddressBinding");
                bugRecord.setDescription("The address has a binding of 0.0.0./*L");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (useOfHTTPWithoutTLS(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("UseOfHTTPWithoutTLS");
                bugRecord.setDescription("The address uses HTTP without TSL");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
            if (weakCryptoAlgo(p, connection)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("WeakCryptoAlgo");
                bugRecord.setDescription("The cryptography algorithm is weak");
                fillContext(bugRecord, p, connection);
                bugs.add(bugRecord);
            }
        }
        bugReport.setActionId(bugInput.getActionId());
        bugReport.setDeploymentId(bugInput.getDeploymentId());
        bugReport.setBugs(bugs);
        return bugReport;
    }

    public void fillContext(BugRecord bugRecord, Feature property, RepositoryConnection connection) throws IOException {
        String sparql = fileToString("sparql/getContext.sparql");
        String query = PREFIXES + sparql;
        IRI var;
        if (property instanceof Comment) {
            var = ((Comment) property).getIri();
        } else {
            var = property.getClassifiedBy();
        }
        TupleQueryResult result = QueryUtil.evaluateSelectQuery(connection,
                query, new SimpleBinding("var", var));
        bugRecord.setElementName(property.getName());
        if (result.hasNext()) {
            BindingSet bindingSet = result.next();
            Binding bindingC = bindingSet.getBinding("context");
            bugRecord.setContext(((IRI) bindingC.getValue()).getLocalName());
            Binding bindingE = bindingSet.getBinding("element");
            bugRecord.setElementType(((SimpleLiteral) bindingE.getValue()).getLabel());
            Binding bindingP = bindingSet.getBinding("pt");
            if (bindingP != null) {
                bugRecord.setElementName(((IRI) bindingP.getValue()).getLocalName());
            }
        }
        result.close();
    }
}
