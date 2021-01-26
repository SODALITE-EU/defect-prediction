import kb.dto.Feature;
import kb.repository.KB;
import kb.repository.SodaliteRepository;
import nl.jads.tosca.DefectPredictorKBApi;
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

public class SecuritySmellAADMTest {
    private static SodaliteRepository repositoryManager;
    private static Repository repository;
    private static KB kb;

    @BeforeAll
    static void beforeAll() throws IOException {
        repositoryManager = new SodaliteRepository(".", "/config.ttl");
        kb = new KB(repositoryManager, "TOSCA");
        repository = repositoryManager.getRepository("TOSCA");
        RepositoryConnection repositoryConnection = repository.getConnection();
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/import/DUL.rdf"), "", RDFFormat.RDFXML);
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/core/sodalite-metamodel.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/core/tosca-builtins.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/snow/snow_tier1.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/snow/snow_tier2.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/snow-aadm/aadm_snow.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.add(SecuritySmellAADMTest.class.getResourceAsStream("/snow-aadm/AADM_as9oa3dfppj6q7irhn6lsl6p16.ttl"), "", RDFFormat.TURTLE);
        repositoryConnection.close();
    }

    @AfterAll
    static void afterAll() {
        repository.shutDown();
        repositoryManager.removeRepository("TOSCA");
        repositoryManager.shutDown("TEST");
    }

    @Test
    void testAdminBYyDefault() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, "AADM_as9oa3dfppj6q7irhn6lsl6p16");
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.adminByDefault(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(2, properties.size());
    }


    @Test
    void testHardcodedSecret() throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi(kb);
        RepositoryConnection connection = repository.getConnection();
        Set<Feature> parameters = kbApi.getProperties(connection, "234333");
        List<Feature> properties = new ArrayList<>();
        for (Feature p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.hardcodedSecret(p, connection)) {
                properties.add(p);
            }
        }
        assertEquals(4, properties.size());
    }

}
