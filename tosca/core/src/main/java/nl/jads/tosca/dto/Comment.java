package nl.jads.tosca.dto;


import kb.dto.Feature;
import org.eclipse.rdf4j.model.IRI;

public class Comment extends Feature {
    private String comment;
    private IRI iri;

    public Comment(IRI iri, String comment) {
        super(iri);
        this.comment = comment;
        this.iri = iri;
    }

    public String getComment() {
        return comment;
    }

    public IRI getIri() {
        return iri;
    }
}
