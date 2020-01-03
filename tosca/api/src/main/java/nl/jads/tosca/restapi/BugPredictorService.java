package nl.jads.tosca.restapi;

import nl.jads.tosca.DefectPredictorKBApi;
import nl.jads.tosca.dto.BugReport;
import nl.jads.tosca.dto.FindBugInput;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.IOException;

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
        BugReport bugReport = kbApi.findBugs(findBugInput);
        kbApi.shutDown();
        return Response.ok(bugReport).build();
    }
}
