package nl.jads.tosca.restapi;

import kb.dto.Property;
import nl.jads.tosca.DefectPredictorKBApi;
import nl.jads.tosca.dto.BugRecord;
import nl.jads.tosca.dto.BugReport;
import nl.jads.tosca.dto.Comment;
import nl.jads.tosca.dto.FindBugInput;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Path("/bugs")
//@Api()
public class BugPredictorService {

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_JSON)
//    @ApiOperation(
//            value = "Returns the bugs in the IaC codes",
////			response = String.class,
//            responseContainer = "List")
    public Response getBugs(FindBugInput findBugInput) throws IOException {
        DefectPredictorKBApi kbApi = new DefectPredictorKBApi();
        BugReport bugReport = findBugs(kbApi,findBugInput);
        kbApi.shutDown();
        return Response.ok(bugReport).build();
    }
    private BugReport findBugs(DefectPredictorKBApi kbApi,FindBugInput bugInput) throws IOException {
        BugReport bugReport = new BugReport();
        List<BugRecord> bugs = new ArrayList<>();
        for (Comment c : kbApi.suspiciousComment()) {
            if (c.getParameters() == null) {
                c.setParameters(new HashSet<>());
            }
            BugRecord bugRecord = new BugRecord();
            bugRecord.setBugName("SuspiciousComment");
            bugRecord.setBugInfo(c);
            bugs.add(bugRecord);
        }
        Set<Property> parameters = kbApi.getProperties();
        for (Property p : parameters) {
            if (p.getParameters() == null) {
                p.setParameters(new HashSet<>());
            }
            if (kbApi.adminByDefault(p)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("AdminByDefault");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (kbApi.emptyPassword(p)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("EmptyPassword");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (kbApi.hardcodedSecret(p)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("HardcodedSecret");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (kbApi.invalidIPAddressBinding(p)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("InvalidIPAddressBinding");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (kbApi.useOfHTTPWithoutTLS(p)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("UseOfHTTPWithoutTLS");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
            if (kbApi.weakCryptoAlgo(p)) {
                BugRecord bugRecord = new BugRecord();
                bugRecord.setBugName("WeakCryptoAlgo");
                bugRecord.setBugInfo(p);
                bugs.add(bugRecord);
            }
        }
        bugReport.setActionId(bugInput.getActionId());
        bugReport.setDeploymentId(bugInput.getDeploymentId());
        bugReport.setBugs(bugs);
        return bugReport;
    }

}
