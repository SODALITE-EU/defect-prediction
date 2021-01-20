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
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Logger;

import static org.junit.Assert.assertEquals;

public class ClinicalSecuritySmellTest {
    private static final java.util.logging.Logger log = Logger.getLogger(ClinicalSecuritySmellTest.class.getName());
    private static SodaliteRepository repositoryManager;
    private static Repository repository;
    private static KB kb;

    @BeforeAll
    static void beforeAll() {
        repositoryManager = new SodaliteRepository(".", "/config_clinical.ttl");
        kb = new KB(repositoryManager, "Clinical");
        repository = repositoryManager.getRepository("Clinical");

        RepositoryConnection repositoryConnection = repository.getConnection();
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    ClinicalSecuritySmellTest.class.getResourceAsStream("/import/DUL.rdf");
            repositoryConnection.add(input, "", RDFFormat.RDFXML);
        } catch (IOException e) {
            log.warning(e.getMessage());
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    ClinicalSecuritySmellTest.class.getResourceAsStream("/core/sodalite-metamodel.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            log.warning(e.getMessage());
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    ClinicalSecuritySmellTest.class.getResourceAsStream("/core/tosca-builtins.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            log.warning(e.getMessage());
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    ClinicalSecuritySmellTest.class.getResourceAsStream("/hpc-clinical-uc-onto-buggy/clinical_tier1.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            log.warning(e.getMessage());
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    ClinicalSecuritySmellTest.class.getResourceAsStream("/hpc-clinical-uc-onto-buggy/clinical_tier2.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            log.warning(e.getMessage());
        }
        repositoryConnection.close();
    }

    @AfterAll
    static void afterAll() {
        repository.shutDown();
        repositoryManager.removeRepository("Clinical");
        repositoryManager.shutDown("TEST");
    }

    @Test
    void testAdminBYyDefault() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
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
            } catch (IOException e) {
                log.warning(e.getMessage());
            }
        } catch (Exception e) {
            log.warning(e.getMessage());
        }
    }

    @Test
    void testSuspiciousComment() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
                List<Comment> comments = kbApi.suspiciousComment(connection);
                assertEquals(1, comments.size());
            } catch (IOException e) {
                log.warning(e.getMessage());
            }
        } catch (Exception e) {
            log.warning(e.getMessage());
        }
    }

    @Test
    void testWeakCryptoAlgo() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
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
            } catch (IOException e) {
                log.warning(e.getMessage());
            }
        } catch (Exception e) {
            log.warning(e.getMessage());
        }
    }

    @Test
    void testInvalidPortRange() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
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
            } catch (IOException e) {
                log.warning(e.getMessage());
            }
        } catch (Exception e) {
            log.warning(e.getMessage());
        }
    }

    @Test
    void testWeakKeySize() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
            RepositoryConnection connection = repository.getConnection();
            try {
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
            } catch (IOException e) {
                log.warning(e.getMessage());
            }
        } catch (Exception e) {
            log.warning(e.getMessage());
        }
    }
}
