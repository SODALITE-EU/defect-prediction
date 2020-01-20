import kb.dto.Property;
import nl.jads.tosca.DefectPredictorKBApi;
import nl.jads.tosca.dto.Comment;
import org.eclipse.rdf4j.model.Resource;
import org.eclipse.rdf4j.model.impl.TreeModel;
import org.eclipse.rdf4j.model.util.Models;
import org.eclipse.rdf4j.model.vocabulary.RDF;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.config.RepositoryConfig;
import org.eclipse.rdf4j.repository.config.RepositoryConfigSchema;
import org.eclipse.rdf4j.repository.manager.LocalRepositoryManager;
import org.eclipse.rdf4j.repository.manager.RepositoryManager;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.eclipse.rdf4j.rio.RDFParser;
import org.eclipse.rdf4j.rio.Rio;
import org.eclipse.rdf4j.rio.helpers.StatementCollector;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.Assert.assertEquals;

public class SecuritySmellTest {
    private static RepositoryManager repositoryManager;
    private static Repository repository;

    @BeforeAll
    static void beforeAll() {
        repositoryManager = new LocalRepositoryManager(new File("."));
        repositoryManager.init();
        TreeModel graph = new TreeModel();
        InputStream config = SecuritySmellTest.class.getResourceAsStream("/config.ttl");
        RDFParser rdfParser = Rio.createParser(RDFFormat.TURTLE);
        rdfParser.setRDFHandler(new StatementCollector(graph));
        try {
            rdfParser.parse(config, RepositoryConfigSchema.NAMESPACE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            config.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        Resource repositoryNode = Models.subject(
                graph.filter(null, RDF.TYPE, RepositoryConfigSchema.REPOSITORY)).orElse(null);

        RepositoryConfig repositoryConfig = RepositoryConfig.create(graph, repositoryNode);
        repositoryManager.addRepositoryConfig(repositoryConfig);

        repository = repositoryManager.getRepository("TOSCA");

        RepositoryConnection repositoryConnection = repository.getConnection();
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/import/DUL.rdf");
            repositoryConnection.add(input, "", RDFFormat.RDFXML);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/core/sodalite-metamodel.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/core/tosca-builtins.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/snow/snow_tier1.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/snow/snow_tier2.ttl");
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
        repositoryManager.shutDown();
    }

    @Test
    void testSuspiciousComment() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                List<Comment> comments = kbApi.suspiciousComment(connection);
                assertEquals(2, comments.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception ignored) {
        }
    }

    @Test
    void testAdminBYyDefault() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection);
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
        } catch (Exception ignored) {
        }
    }

    @Test
    void testEmptyPassword() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection);
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.emptyPassword(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(1, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception ignored) {
        }
    }

    @Test
    void testHardcodedSecret() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection);
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.hardcodedSecret(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(2, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception ignored) {
        }
    }

    @Test
    void testUseOfHTTPWithoutTLS() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection);
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.useOfHTTPWithoutTLS(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(1, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception ignored) {
        }
    }

    @Test
    void testWeakCryptoAlgo() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection);
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.weakCryptoAlgo(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(1, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception ignored) {
        }
    }

    @Test
    void testInvalidIPAddressBinding() {
        try {
            DefectPredictorKBApi kbApi = new DefectPredictorKBApi(repository);
            RepositoryConnection connection = repository.getConnection();
            try {
                Set<Property> parameters = kbApi.getProperties(connection);
                List<Property> properties = new ArrayList<>();
                for (Property p : parameters) {
                    if (p.getParameters() == null) {
                        p.setParameters(new HashSet<>());
                    }
                    if (kbApi.invalidIPAddressBinding(p, connection)) {
                        properties.add(p);
                    }
                }
                assertEquals(1, properties.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception ignored) {
        }
    }
}
