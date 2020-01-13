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
import java.util.List;

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
                    SecuritySmellTest.class.getResourceAsStream("/ontology/DUL.rdf");
            repositoryConnection.add(input, "", RDFFormat.RDFXML);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/ontology/sodalite-metamodel.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/ontology/tosca-builtins.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // add the RDF data from the inputstream directly to our database
        try {
            InputStream input =
                    SecuritySmellTest.class.getResourceAsStream("/ontology/snow-blueprint-containerized-OS.ttl");
            repositoryConnection.add(input, "", RDFFormat.TURTLE);
        } catch (IOException e) {
            e.printStackTrace();
        }
        repositoryConnection.close();
    }

    @AfterAll
    static void afterAll() {
        repository.shutDown();
        repositoryManager.shutDown();
    }

    @Test
    void testSuspiciousComment() {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi();
        RepositoryConnection connection = repository.getConnection();
        try {
            List<Comment> comments = kbApi.suspiciousComment(connection);
            assertEquals(2, comments.size());
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
