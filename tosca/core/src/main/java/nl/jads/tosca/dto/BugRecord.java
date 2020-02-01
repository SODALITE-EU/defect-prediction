package nl.jads.tosca.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import kb.dto.Feature;

@JsonNaming(PropertyNamingStrategy.SnakeCaseStrategy.class)
public class BugRecord {
    private String bugName;
    private String elementType;
    private String elementName;
    private String context;
    private Feature bugInfo;
    private String description;

    public String getBugName() {
        return bugName;
    }

    public void setBugName(String bugName) {
        this.bugName = bugName;
    }

    public Feature getBugInfo() {
        return bugInfo;
    }

    public void setBugInfo(Feature bugInfo) {
        this.bugInfo = bugInfo;
    }

    public String getElementType() {
        return elementType;
    }

    public void setElementType(String elementType) {
        this.elementType = elementType;
    }

    public String getElementName() {
        return elementName;
    }

    public void setElementName(String elementName) {
        this.elementName = elementName;
    }

    public String getContext() {
        return context;
    }

    public void setContext(String context) {
        this.context = context;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
