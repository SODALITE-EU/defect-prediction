import kb.dto.Feature;
import kb.repository.KB;
import kb.repository.SodaliteRepository;
import nl.jads.tosca.DefectPredictorKBApi;
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

public class ClinicalSecuritySmellTest {
    private static SodaliteRepository repositoryManager;
    private static Repository repository;
    private static KB kb;

    @BeforeAll
    static void beforeAll() throws IOException {
        repositoryManager = new SodaliteRepository(".", "/config_clinical.ttl");
        kb = new KB(repositoryManager, "Clinical");
        repository = repositoryManager.getRepository("Clinical");
        RepositoryConnection repositoryConnection = repository.getConnection();
        repositoryConnection.add(ClinicalSecuritySmellTest.class.getResourceAsStream("/import/DUL.rdf"), "", RDFFormat.RDFXML);
        repositoryConnection.add(ClinicalSecuritySmellTest.class.getResourceAsStream("/core/sodalite-metamodel.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(ClinicalSecuritySmellTest.class.getResourceAsStream("/core/tosca-builtins.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(ClinicalSecuritySmellTest.class.getResourceAsStream("/hpc-clinical-uc-onto-buggy/clinical_tier1.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(ClinicalSecuritySmellTest.class.getResourceAsStream("/hpc-clinical-uc-onto-buggy/clinical_tier2.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.close();
    }

    @AfterAll
    static void afterAll() {
        repository.shutDown();
        repositoryManager.removeRepository("Clinical");
        repositoryManager.shutDown("TEST");
    }

    @Test
    void testAdminBYyDefault() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getAllAttributes(connection, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.adminByDefault(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }

    @Test
    void testSuspiciousComment() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        List<Comment> comments = kbApi.suspiciousComment(connection);
        assertEquals(1, comments.size());
    }

    @Test
    void testWeakCryptoAlgo() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getAllAttributes(connection, null);
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
    void testInvalidPortRange() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getAllAttributes(connection, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.invalidPortRange(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }

    @Test
    void testWeakKeySize() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getAllAttributes(connection, null);
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.weakKeySize(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(1, properties.size());
    }
}
