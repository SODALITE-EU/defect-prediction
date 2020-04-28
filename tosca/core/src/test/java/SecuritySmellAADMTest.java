import kb.dto.Property;
import kb.repository.KB;
import kb.repository.SodaliteRepository;
import nl.jads.tosca.DefectPredictorKBApi;
import nl.jads.tosca.dto.BugRecord;
import nl.jads.tosca.dto.Comment;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.Assert.assertEquals;

public class SecuritySmellAADMTest {
    private static SodaliteRepository repositoryManager;
    private static Repository repository;
    private static KB kb;

    @BeforeAll
    static void beforeAll() {
        repositoryManager = new SodaliteRepository(".", "/config.ttl");
        kb = new KB(repositoryManager, "TOSCA");

        repository = repositoryManager.getRepository("TOSCA");

        RepositoryConnection repositoryConnection = repository.getConnection();
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellAADMTest.class.getResourceAsStream("/import/DUL.rdf");
            repositoryConnection.add(input, "", RDFFormat.RDFXML);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellAADMTest.class.getResourceAsStream("/core/sodalite-metamodel.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellAADMTest.class.getResourceAsStream("/core/tosca-builtins.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellAADMTest.class.getResourceAsStream("/snow/snow_tier1.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellAADMTest.class.getResourceAsStream("/snow/snow_tier2.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellAADMTest.class.getResourceAsStream("/snow-aadm/aadm_snow.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        repositoryConnection.close();
    }

    @AfterAll
    static void afterAll() {
        repository.shutDown();
        repositoryManager.removeRepository("TOSCA");
        repositoryManager.shutDown("TEST");
    }

//    @Test
//    void testSuspiciousComment() {
//        try {
//            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
//            RepositoryConnection connection = repository.getConnection();
//            try {
//                List<Comment> comments = kbApi.suspiciousComment(connection);
//                assertEquals(3, comments.size());
//                for (Comment c : comments) {
//                    BugRecord r = new BugRecord();
//                    kbApi.fillContext(r, c, connection);
//                    System.out.println(r.getElementType());
//                    System.out.println(r.getElementName());
//                    System.out.println(r.getContext());
//                }
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }

    @Test
    void testAdminBYyDefault() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection, "234333");
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.adminByDefault(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(1, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    @Test
    void testHardcodedSecret() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection, "234333");
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.hardcodedSecret(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(1, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
