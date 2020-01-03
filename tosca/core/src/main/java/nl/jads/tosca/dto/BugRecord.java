package nl.jads.tosca.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import kb.dto.Feature;

@JsonNaming(PropertyNamingStrategy.SnakeCaseStrategy.class)
public class BugRecord {
    private String bugName;
    private Feature bugInfo;

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
}
