package nl.jads.tosca.dto;


import kb.dto.Feature;
import org.eclipse.rdf4j.model.IRI;

public class Comment extends Feature {
    private String comment;

    public Comment(IRI iri, String comment) {
        super(iri);
        this.comment = comment;
    }

    public String getComment() {
        return comment;
    }
}
