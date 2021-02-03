import kb.dto.Feature;
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
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.Assert.assertEquals;

public class SecuritySmellTest {
    private static SodaliteRepository repositoryManager;
    private static Repository repository;
    private static KB kb;

    @BeforeAll
    static void beforeAll() throws IOException {
        repositoryManager = new SodaliteRepository("target/", "/config.ttl");
        kb = new KB(repositoryManager, "TOSCA");
        repository = repositoryManager.getRepository("TOSCA");
        RepositoryConnection repositoryConnection = repository.getConnection();
        repositoryConnection.add(SecuritySmellTest.class.getResourceAsStream("/import/DUL.rdf"), "", RDFFormat.RDFXML);
        repositoryConnection.add(SecuritySmellTest.class.getResourceAsStream("/core/sodalite-metamodel.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellTest.class.getResourceAsStream("/core/tosca-builtins.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellTest.class.getResourceAsStream("/snow/snow_tier1.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellTest.class.getResourceAsStream("/snow/snow_tier2.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.close();
    }

    @AfterAll
    static void afterAll() {
        repository.shutDown();
        repositoryManager.removeRepository("TOSCA");
        repositoryManager.shutDown("TEST");
    }

    @Test
    void testSuspiciousComment() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        List<Comment> comments = kbApi.suspiciousComment(connection);
        assertEquals(3, comments.size());
        for (Comment c : comments) {
            BugRecord r = new BugRecord();
            kbApi.fillContext(r, c, connection);
        }
    }

    @Test
    void testAdminBYyDefault() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.adminByDefault(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(3, properties.size());
    }

    @Test
    void testDashCaseViolation() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        List<Feature> properties2 = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.isDashCase(p, connection)) {
                properties.add(p);
            } else {
                properties2.add(p);
            }
        }
        assertEquals(2, properties.size());
        assertEquals(78, properties2.size());
    }

    @Test
    void testSnakeCaseViolation() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        List<Feature> properties2 = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.isSnakeCase(p, connection)) {
                properties.add(p);
            } else {
                properties2.add(p);
            }
        }
        assertEquals(40, properties.size());
        assertEquals(40, properties2.size());
    }

    @Test
    void testCamelCaseViolation() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        List<Feature> properties2 = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.isCamelCase(p, connection)) {
                properties.add(p);
                System.out.println("*******" + p);
            } else {
                properties2.add(p);
            }
        }
        assertEquals(1, properties.size());
        assertEquals(79, properties2.size());
    }

    @Test
    void testEmptyPassword() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.emptyPassword(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }

    @Test
    void testHardcodedSecret() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.hardcodedSecret(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(5, properties.size());
    }

    @Test
    void testUseOfHTTPWithoutTLS() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.useOfHTTPWithoutTLS(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }

    @Test
    void testWeakCryptoAlgo() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.weakCryptoAlgo(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }

    @Test
    void testInvalidIPAddressBinding() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, null, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.invalidIPAddressBinding(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }
}
