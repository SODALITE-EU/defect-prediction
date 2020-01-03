package nl.jads.tosca.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

@JsonNaming(PropertyNamingStrategy.SnakeCaseStrategy.class)
public class FindBugInput {
    private String actionId;
    private String deploymentId;
    private String toscaDefinition;
    private String ansibleDefinition;

    public String getActionId() {
        return actionId;
    }

    public void setActionId(String actionId) {
        this.actionId = actionId;
    }

    public String getDeploymentId() {
        return deploymentId;
    }

    public void setDeploymentId(String deploymentId) {
        this.deploymentId = deploymentId;
    }

    public String getToscaDefinition() {
        return toscaDefinition;
    }

    public void setToscaDefinition(String toscaDefinition) {
        this.toscaDefinition = toscaDefinition;
    }

    public String getAnsibleDefinition() {
        return ansibleDefinition;
    }

    public void setAnsibleDefinition(String ansibleDefinition) {
        this.ansibleDefinition = ansibleDefinition;
    }
}
